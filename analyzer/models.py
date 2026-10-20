from django.db import models


class AnalysisResult(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]

    text = models.TextField(verbose_name="Text")
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, verbose_name="Sentiment")
    confidence = models.FloatField(verbose_name="Confidence")
    latency_ms = models.FloatField(null=True, blank=True, verbose_name="Latency (ms)")
    memory_mb = models.FloatField(null=True, blank=True, verbose_name="Memory Usage (MB)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Analysis Result"
        verbose_name_plural = "Analysis Results"

    def __str__(self):
        return f"{self.get_sentiment_display()} - {self.confidence:.2f}"