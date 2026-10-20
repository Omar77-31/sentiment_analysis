import os
import time
import logging

import psutil
import torch
from functools import lru_cache
from transformers import pipeline
from django.conf import settings

logger = logging.getLogger(__name__)


LABEL_MAP = {
    "positive": "positive",
    "negative": "negative",
    "neutral": "neutral",
}


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    """Load the model once and cache it in memory."""
    model_name = settings.SENTIMENT_MODEL
    device = 0 if torch.cuda.is_available() else -1
    logger.info("Loading model: %s on %s...", model_name, "GPU" if device == 0 else "CPU")
    return pipeline(
        "sentiment-analysis",
        model=model_name,
        tokenizer=model_name,
        device=device,
    )


def normalize_label(label: str) -> str:
    """Normalize model output label to positive / negative / neutral.

    Raises ValueError for any unexpected label so a silent
    mis-classification can never reach the database.
    """
    key = str(label).strip().lower()
    if key not in LABEL_MAP:
        raise ValueError(f"Unexpected model label: {label!r}")
    return LABEL_MAP[key]


def analyze_text(text: str) -> dict:
    """Analyze text and return sentiment with metrics."""
    text = (text or "").strip()
    if not text:
        raise ValueError("Text is empty")


    clf = get_sentiment_pipeline()

    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024

    start = time.perf_counter()
    raw = clf(text, truncation=True, max_length=512)[0]
    latency_ms = (time.perf_counter() - start) * 1000

    mem_after = process.memory_info().rss / 1024 / 1024

    return {
        "sentiment": normalize_label(raw["label"]),
        "confidence": float(raw["score"]),
        "latency_ms": latency_ms,
        "memory_mb": mem_after - mem_before,
    }