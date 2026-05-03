import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME             = "t5-base"
MAX_INPUT_LEN          = 512
NUM_BEAMS              = 4
MIN_WORDS_TO_SUMMARIZE = 40

device       = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Loading {MODEL_NAME} on {device}...")
tokenizer_t5 = AutoTokenizer.from_pretrained(MODEL_NAME)
model_t5     = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(device)
model_t5.eval()
print("T5-base ready.")


def summarize(text: str) -> str:
    # Fix 17: input validation
    if not isinstance(text, str) or not text.strip():
        return ""

    word_count = len(text.split())
    if word_count < MIN_WORDS_TO_SUMMARIZE:
        return text.strip()

    prefixed = "summarize: " + text

    inputs = tokenizer_t5(
        prefixed,
        return_tensors="pt",
        max_length=MAX_INPUT_LEN,
        truncation=True,
    ).to(device)

    input_len = inputs["input_ids"].shape[1]
    max_sum   = min(150, max(30, input_len // 3))
    min_sum   = min(30,  max(10, input_len // 6))

    with torch.no_grad():
        ids = model_t5.generate(
            inputs.input_ids,
            max_length           = max_sum,
            min_length           = min_sum,
            num_beams            = NUM_BEAMS,
            length_penalty       = 1.0,
            no_repeat_ngram_size = 3,
            early_stopping       = True,
        )

    return tokenizer_t5.decode(ids[0], skip_special_tokens=True)


demo = gr.Interface(
    fn=summarize,
    inputs=gr.Textbox(label="Complaint text(s) to summarize", lines=8),
    outputs=gr.Textbox(label="Summary"),
    title="T5 Summarizer — CFPB Complaints",
    description="Abstractive summarization with dynamic length control.",
)

if __name__ == "__main__":
    demo.launch()
