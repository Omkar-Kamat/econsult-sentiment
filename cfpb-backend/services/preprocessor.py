from __future__ import annotations
import re
import nltk
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

for pkg in ["stopwords", "wordnet", "punkt"]:
    nltk.download(pkg, quiet=True)

nlp    = spacy.load("en_core_web_sm", disable=["parser", "ner"])
vader  = SentimentIntensityAnalyzer()

DOMAIN_STOP = {
    "company", "account", "consumer", "bank", "told", "would",
    "said", "called", "also", "get", "got", "one", "us", "go",
}
STOP_WORDS = set(stopwords.words("english")) | DOMAIN_STOP


def clean_text(text: str) -> str:
    """Apply the NB03 cleaning pipeline to a raw narrative string."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+\.\S+", " ", text)
    text = re.sub(r"x{2,}", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def lemmatize(text: str) -> str:
    """Lemmatize and remove stopwords using spaCy (NB03 logic)."""
    doc = nlp(text)
    tokens = [
        t.lemma_ for t in doc
        if t.lemma_ not in STOP_WORDS
        and len(t.lemma_) > 2
        and t.lemma_.isalpha()
    ]
    return " ".join(tokens)


def vader_sentiment(text: str) -> dict:
    """Return VADER compound score and 3-class label."""
    scores  = vader.polarity_scores(text)
    compound = scores["compound"]
    label = (
        "positive" if compound >= 0.05
        else "negative" if compound <= -0.05
        else "neutral"
    )
    return {
        "compound":      round(compound, 4),
        "sentiment":     label,
        "prob_negative": round(max(0.0, -compound), 4),
        "prob_neutral":  round(1.0 - abs(compound), 4),
        "prob_positive": round(max(0.0,  compound), 4),
    }


def count_redactions(narrative: str) -> int:
    return len(re.findall(r"X{2,}", str(narrative)))


def preprocess(narrative: str) -> dict:
    """Full preprocessing pipeline for a single narrative."""
    text_clean     = clean_text(narrative)
    text_processed = lemmatize(text_clean)
    word_count     = len(text_clean.split())
    redaction_count = count_redactions(narrative)

    sentiment_data = vader_sentiment(text_clean)

    return {
        "text_clean":       text_clean,
        "text_processed":   text_processed,
        "word_count":       word_count,
        "redaction_count":  redaction_count,
        "redaction_density": redaction_count / max(word_count, 1),
        **sentiment_data,
    }