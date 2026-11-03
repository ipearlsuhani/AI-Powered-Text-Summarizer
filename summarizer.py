from functools import lru_cache
from transformers import pipeline

MODEL_NAME = "sshleifer/distilbart-cnn-6-6"

@lru_cache(maxsize=1)
def get_summarizer():
    """Load the pretrained model once per app process."""
    return pipeline("summarization", model=MODEL_NAME, device=-1)

def summarize_text(text):
    """Summarize long input in token-safe chunks, then combine chunk summaries."""
    if not text or not text.strip():
        return "Please enter some text."

    model = get_summarizer()
    tokenizer = model.tokenizer

    # Keep each input safely below DistilBART's encoder token limit.
    token_ids = tokenizer.encode(text, add_special_tokens=False)
    chunk_size = 850
    chunks = [
        tokenizer.decode(token_ids[i:i + chunk_size], skip_special_tokens=True)
        for i in range(0, len(token_ids), chunk_size)
    ]

    partial_summaries = []
    for chunk in chunks:
        ids_count = len(tokenizer.encode(chunk, add_special_tokens=True))
        max_len = min(130, max(35, ids_count - 2))
        min_len = min(30, max(8, max_len // 3))
        result = model(
            chunk,
            max_length=max_len,
            min_length=min_len,
            do_sample=False,
            truncation=True
        )
        partial_summaries.append(result[0]["summary_text"].strip())

    combined = " ".join(partial_summaries)

    # If many chunks produce a long combined text, summarize that text in
    # another safe pass. This avoids silently discarding later document pages.
    while len(tokenizer.encode(combined, add_special_tokens=False)) > 850:
        ids = tokenizer.encode(combined, add_special_tokens=False)
        groups = [
            tokenizer.decode(ids[i:i + 850], skip_special_tokens=True)
            for i in range(0, len(ids), 850)
        ]
        reduced = []
        for group in groups:
            result = model(
                group,
                max_length=130,
                min_length=30,
                do_sample=False,
                truncation=True
            )
            reduced.append(result[0]["summary_text"].strip())
        combined = " ".join(reduced)

    return combined
