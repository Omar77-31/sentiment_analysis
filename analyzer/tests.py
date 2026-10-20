from django.test import TestCase
from django.urls import reverse
from .models import AnalysisResult
from unittest.mock import patch


class AnalyzerTests(TestCase):


    def test_history_pagination(self):
        for i in range(25):
            AnalysisResult.objects.create(
                text=f"نص {i}", sentiment="neutral", confidence=0.8
            )
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['results']), 20)


    def test_api_requires_arabic(self):
        response = self.client.post(reverse('api_analyze'), {"text": "Hello"})
        self.assertEqual(response.status_code, 400)


    def test_api_blank_text(self):
        response = self.client.post(reverse('api_analyze'), {"text": ""})
        self.assertEqual(response.status_code, 400)


    @patch('analyzer.views.analyze_text')
    def test_api_success(self, mock_analyze):
        mock_analyze.return_value = {
            "sentiment": "positive",
            "confidence": 0.99,
            "latency_ms": 100.0,
            "memory_mb": 5.0
        }
        response = self.client.post(reverse('api_analyze'), {"text": "هذا المنتج رائع"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AnalysisResult.objects.count(), 1)
        self.assertEqual(AnalysisResult.objects.first().sentiment, "positive")