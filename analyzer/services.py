import os
import time
import psutil
import torch
from functools import lru_cache
from transformers import pipeline
from django.conf import settings


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    """Load the model once and cache it in memory."""
    model_name = settings.SENTIMENT_MODEL
    device = 0 if torch.cuda.is_available() else -1
    print(f"Loading model: {model_name} on {'GPU' if device == 0 else 'CPU'}...")
    return pipeline(
        "sentiment-analysis",
        model=model_name,
        tokenizer=model_name,
        device=device,
    )


def normalize_label(label: str) -> str:
    """Normalize model output labels to positive/negative only."""
    label = str(label).lower()
    if "pos" in label:
        return "positive"
    return "negative"


def analyze_text(text: str) -> dict:
    """Analyze text and return sentiment with metrics."""
    text = (text or "").strip()
    if not text:
        raise ValueError("Text is empty")

    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024

    start = time.perf_counter()
    clf = get_sentiment_pipeline()
    raw = clf(text, truncation=True, max_length=512)[0]
    latency_ms = (time.perf_counter() - start) * 1000

    mem_after = process.memory_info().rss / 1024 / 1024

    label = normalize_label(raw["label"])
    confidence = float(raw["score"])

    return {
        "sentiment": label,
        "confidence": confidence,
        "latency_ms": latency_ms,
        "memory_mb": mem_after - mem_before,
    }