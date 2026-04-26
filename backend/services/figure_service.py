from pathlib import Path
from core.config import settings

FIGURE_CATALOG = {
    "01_class_distributions": {
        "title": "Complaint Class Distributions",
        "subtitle": "Product category balance and company response types across the 20,000-row sample.",
        "notebook": "NB02 — Exploratory Data Analysis",
        "note": (
            "Credit Reporting was capped at 40% during stratified sampling (NB01) "
            "to prevent it from dominating downstream models."
        ),
    },
    "02_word_count_analysis": {
        "title": "Complaint Word Count Analysis",
        "subtitle": "Word count histogram (all complaints) and per-product box plots.",
        "notebook": "NB02 — Exploratory Data Analysis",
        "note": (
            "The median complaint is 91 words. 95th percentile is 247 words. "
            "This guided the BERT MAX_LEN=128 configuration in NB05."
        ),
    },
    "03_issue_breakdown": {
        "title": "Top Issues per Product Category",
        "subtitle": "Top-5 most common issue types broken down by product category.",
        "notebook": "NB02 — Exploratory Data Analysis",
        "note": (
            "Each product category has a genuinely distinct issue profile, "
            "confirming that clustering by complaint language is feasible."
        ),
    },
    "03_vader_sentiment": {
        "title": "VADER Sentiment Distribution",
        "subtitle": "Compound sentiment score histogram with ±0.05 threshold lines.",
        "notebook": "NB03 — Text Preprocessing",
        "note": (
            "VADER labels served as training targets for BERT (NB05). "
            "The majority of complaints score negative, as expected."
        ),
    },
    "04_k_selection": {
        "title": "Optimal Cluster Count Selection",
        "subtitle": "Silhouette score vs k (left) and inertia elbow plot (right).",
        "notebook": "NB04 — Topic Clustering",
        "note": (
            "Silhouette analysis over k=3 to 10 confirmed k=3 as optimal. "
            "Higher silhouette = tighter, more distinct clusters."
        ),
    },
    "04_umap_visualization": {
        "title": "UMAP Complaint Landscape",
        "subtitle": "2-D projection of all 20,000 complaints coloured by cluster, product, and sentiment.",
        "notebook": "NB04 — Topic Clustering",
        "note": (
            "UMAP preserves local semantic neighbourhoods. Visually distinct colour "
            "groups confirm the three clusters have genuine separable structure."
        ),
    },
    "05_training_history": {
        "title": "BERT Training History",
        "subtitle": "Loss curves and accuracy/F1 curves across 3 fine-tuning epochs.",
        "notebook": "NB05 — Sentiment Classification with BERT",
        "note": (
            "Trained on bert-base-uncased (110M parameters) with AdamW, "
            "linear warmup, and class-weighted CrossEntropy loss."
        ),
    },
    "05_confusion_matrix": {
        "title": "BERT Sentiment Confusion Matrix",
        "subtitle": "Counts and normalized confusion matrices on the held-out test set.",
        "notebook": "NB05 — Sentiment Classification with BERT",
        "note": (
            "The model performs strongest on the negative class (most training data). "
            "Neutral and positive show higher inter-class confusion."
        ),
    },
    "06_rouge_scores": {
        "title": "T5 Summary Consistency (ROUGE Scores)",
        "subtitle": "Pairwise ROUGE-1/2/L scores comparing 5 independent summary batches per cluster.",
        "notebook": "NB06 — Abstractive Summarisation with T5",
        "note": (
            "High pairwise ROUGE scores indicate T5 consistently identifies the same "
            "themes regardless of which complaints it samples — validating cluster coherence."
        ),
    },
    "06_wordclouds": {
        "title": "Cluster Word Clouds",
        "subtitle": "Dominant vocabulary for each of the 3 complaint clusters.",
        "notebook": "NB06 — Abstractive Summarisation with T5",
        "note": (
            "Word size represents TF-IDF-weighted term frequency within the cluster. "
            "Confirms distinct lexical profiles: bureau/dispute, debt/collector, payment/charge."
        ),
    },
}


def get_figure_path(key: str) -> Path | None:
    if key not in FIGURE_CATALOG:
        return None
    path = Path(settings.static_figures_dir) / f"{key}.png"
    return path if path.exists() else None


def get_all_figure_metadata(base_url: str) -> list:
    return [
        {
            "key": key,
            "url": f"{base_url}/api/v1/figures/{key}",
            **meta,
        }
        for key, meta in FIGURE_CATALOG.items()
    ]