from django.urls import path
from .views import IndexView, HistoryView, AnalyzeAPIView


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("history/", HistoryView.as_view(), name="history"),
    path("api/analyze/", AnalyzeAPIView.as_view(), name="api_analyze"),
]