import re
import string
from typing import List
import spacy
from nltk.corpus import stopwords

DOMAIN_STOP_WORDS = {
    "company", "account", "bank", "consumer", "told", "said",
    "would", "also", "one", "call", "payment", "loan",
    "report", "financial",
}

NLTK_STOP_WORDS = set(stopwords.words("english"))
ALL_STOP_WORDS = NLTK_STOP_WORDS | DOMAIN_STOP_WORDS


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\bxx+\b", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def lemmatize_batch(texts: List[str], nlp: spacy.Language, batch_size: int = 512) -> List[str]:
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        docs = list(nlp.pipe(batch, batch_size=min(batch_size, len(batch))))
        for doc in docs:
            tokens = [
                token.lemma_
                for token in doc
                if (
                    token.is_alpha
                    and len(token.text) > 2
                    and token.lemma_ not in ALL_STOP_WORDS
                )
            ]
            results.append(" ".join(tokens))
    return results