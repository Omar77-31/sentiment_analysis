from django.contrib import admin
from .models import AnalysisResult


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ("id", "sentiment", "confidence", "latency_ms", "created_at")
    list_filter = ("sentiment", "created_at")
    search_fields = ("text",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)