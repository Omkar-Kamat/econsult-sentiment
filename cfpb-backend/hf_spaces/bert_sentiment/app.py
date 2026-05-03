import gradio as gr
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_DIR   = "./model"           # ← changed from "./bert_sentiment"
MAX_LEN     = 128
LABEL_NAMES = ["negative", "neutral", "positive"]

device    = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model     = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR).to(device)
model.eval()

print(f"BERT sentiment loaded on {device}")


def predict_sentiment(text: str) -> dict:
    if not isinstance(text, str) or not text.strip():
        return {"label": "neutral", "probs": [0.0, 1.0, 0.0]}

    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=MAX_LEN,
        padding="max_length",
        truncation=True,
    )
    input_ids      = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    with torch.no_grad():
        logits = model(input_ids, attention_mask=attention_mask).logits
        probs  = torch.softmax(logits, dim=1).cpu().numpy()[0]

    label = LABEL_NAMES[int(probs.argmax())]
    return {
        "label": label,
        "probs": [round(float(p), 4) for p in probs],
    }


demo = gr.Interface(
    fn=predict_sentiment,
    inputs=gr.Textbox(label="Complaint text"),
    outputs=gr.JSON(label="Sentiment result"),
    title="BERT Sentiment — CFPB Complaints",
    description="Returns label (negative/neutral/positive) and class probabilities.",
)

if __name__ == "__main__":
    demo.launch()