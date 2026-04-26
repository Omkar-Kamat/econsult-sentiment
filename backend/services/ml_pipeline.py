import time
import logging
import joblib
import numpy as np
import torch
from pathlib import Path
from sentence_transformers import SentenceTransformer
from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    T5Tokenizer,
    T5ForConditionalGeneration,
)
from core.config import settings
from services.preprocessing import clean_text, lemmatize_batch
import spacy

logger = logging.getLogger(__name__)

CLUSTER_METADATA = {
    0: {
        "label": "Credit Report Disputes",
        "keywords": [
            "credit report", "dispute", "bureau", "incorrect", "account",
            "information", "remove", "inquiry", "collection", "negative"
        ],
        "product_hint": "Credit Reporting",
        "tone": "formal-apologetic",
        "context": (
            "This complaint relates to incorrect or fraudulent information "
            "appearing on the consumer's credit report. Common issues include "
            "accounts not belonging to the consumer, incorrect balances, and "
            "failed or ignored bureau dispute attempts."
        ),
        "suggested_actions": [
            "Initiate a formal dispute with all three credit bureaus (Equifax, Experian, TransUnion)",
            "Provide the consumer with a case reference number and 30-day resolution timeline",
            "Request supporting documentation from the consumer (proof of identity, account statements)",
            "Escalate to Credit Operations team if the account is flagged as potential fraud",
        ],
    },
    1: {
        "label": "Debt Collection & Recovery",
        "keywords": [
            "debt", "collection", "collector", "payment", "call", "letter",
            "validate", "owe", "contact", "harassment"
        ],
        "product_hint": "Debt Collection",
        "tone": "formal-resolving",
        "context": (
            "This complaint relates to debt collection practices. Common issues "
            "include collectors contacting consumers at inappropriate times, "
            "attempting to collect debts the consumer does not owe, failure to "
            "provide debt validation, and aggressive or harassing contact."
        ),
        "suggested_actions": [
            "Issue a formal debt validation letter within 5 business days per FDCPA requirements",
            "Place a cease-and-desist hold on all outbound contact pending investigation",
            "Review collection account history and verify original creditor documentation",
            "Confirm consumer's right to dispute the debt in writing within 30 days",
        ],
    },
    2: {
        "label": "Card Payments & Account Calls",
        "keywords": [
            "payment", "charge", "card", "account", "fee", "statement",
            "credit card", "balance", "interest", "billing"
        ],
        "product_hint": "Credit Card",
        "tone": "formal-informational",
        "context": (
            "This complaint relates to credit card billing, payments, or account "
            "management. Common issues include unauthorized charges, disputed "
            "transactions, billing errors, excessive fees, and difficulty reaching "
            "account services."
        ),
        "suggested_actions": [
            "Review the last 90 days of transaction history on the account",
            "Initiate a chargeback investigation for any disputed transactions",
            "Apply provisional credit to the account within 5 business days if applicable",
            "Confirm correct fee schedule and apply waivers where appropriate",
        ],
    },
}

SENTIMENT_LABELS = {0: "negative", 1: "neutral", 2: "positive"}


class MLPipeline:
    def __init__(self):
        self._loaded = False
        self.nlp = None
        self.tfidf = None
        self.kmeans = None
        self.umap_reducer = None
        self.encoder = None
        self.bert_tokenizer = None
        self.bert_model = None
        self.t5_tokenizer = None
        self.t5_model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load(self):
        if self._loaded:
            logger.info("ML Pipeline already loaded — skipping.")
            return

        artifacts_dir = Path(settings.ml_artifacts_dir)
        logger.info(f"Loading ML artifacts from: {artifacts_dir} | Device: {self.device}")

        t = time.time()
        self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        logger.info(f"  spaCy loaded ({time.time() - t:.2f}s)")

        t = time.time()
        self.tfidf = joblib.load(artifacts_dir / "tfidf_vectorizer.pkl")
        logger.info(f"  TF-IDF vectorizer loaded ({time.time() - t:.2f}s)")

        t = time.time()
        self.kmeans = joblib.load(artifacts_dir / "kmeans_k3.pkl")
        logger.info(f"  K-Means model loaded ({time.time() - t:.2f}s)")

        t = time.time()
        self.umap_reducer = joblib.load(artifacts_dir / "umap_reducer.pkl")
        logger.info(f"  UMAP reducer loaded ({time.time() - t:.2f}s)")

        t = time.time()
        self.encoder = SentenceTransformer(settings.sentence_transformer_model)
        self.encoder.to(self.device)
        logger.info(f"  SentenceTransformer loaded ({time.time() - t:.2f}s)")

        t = time.time()
        self.bert_tokenizer = BertTokenizer.from_pretrained(settings.bert_model_path)
        self.bert_model = BertForSequenceClassification.from_pretrained(settings.bert_model_path,use_safetensors=True)
        self.bert_model.to(self.device)
        self.bert_model.eval()
        logger.info(f"  BERT sentiment model loaded ({time.time() - t:.2f}s)")

        t = time.time()
        self.t5_tokenizer = T5Tokenizer.from_pretrained(settings.t5_model_name)
        self.t5_model = T5ForConditionalGeneration.from_pretrained(settings.t5_model_name)
        self.t5_model.to(self.device)
        self.t5_model.eval()
        logger.info(f"  T5 model loaded ({time.time() - t:.2f}s)")

        self._loaded = True
        logger.info("All ML artifacts loaded successfully.")

    def preprocess(self, raw_text: str) -> dict:
        text_clean = clean_text(raw_text)
        text_processed = lemmatize_batch([text_clean], self.nlp)[0]
        return {
            "text_clean": text_clean,
            "text_processed": text_processed,
            "word_count": len(raw_text.split()),
        }

    def classify(self, raw_text: str) -> dict:
        start = time.time()

        prep = self.preprocess(raw_text)

        embedding = self.encoder.encode(
            [prep["text_processed"]],
            normalize_embeddings=True,
            device=self.device,
            show_progress_bar=False,
        )

        cluster_id = int(self.kmeans.predict(embedding)[0])
        cluster_meta = CLUSTER_METADATA[cluster_id]

        encoded = self.bert_tokenizer(
            prep["text_clean"],
            max_length=128,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        input_ids = encoded["input_ids"].to(self.device)
        attention_mask = encoded["attention_mask"].to(self.device)

        with torch.no_grad():
            outputs = self.bert_model(input_ids=input_ids, attention_mask=attention_mask)
            probs = torch.softmax(outputs.logits, dim=1).cpu().numpy()[0]

        sentiment_idx = int(np.argmax(probs))
        sentiment_label = SENTIMENT_LABELS[sentiment_idx]

        processing_ms = int((time.time() - start) * 1000)

        return {
            "text_clean": prep["text_clean"],
            "text_processed": prep["text_processed"],
            "word_count": prep["word_count"],
            "embedding": embedding[0].tolist(),
            "cluster_id": cluster_id,
            "cluster_label": cluster_meta["label"],
            "cluster_keywords": cluster_meta["keywords"],
            "product_hint": cluster_meta["product_hint"],
            "sentiment": sentiment_label,
            "sentiment_scores": {
                "negative": round(float(probs[0]), 4),
                "neutral": round(float(probs[1]), 4),
                "positive": round(float(probs[2]), 4),
            },
            "sentiment_confidence": round(float(probs[sentiment_idx]), 4),
            "processing_ms": processing_ms,
        }

    def summarize(self, text: str, max_length: int = 150, min_length: int = 60) -> str:
        prompt = f"summarize: {text}"
        inputs = self.t5_tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True,
        ).to(self.device)

        with torch.no_grad():
            output_ids = self.t5_model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_length=max_length,
                min_length=min_length,
                num_beams=4,
                no_repeat_ngram_size=3,
                early_stopping=True,
            )

        return self.t5_tokenizer.decode(output_ids[0], skip_special_tokens=True)


ml_pipeline = MLPipeline()