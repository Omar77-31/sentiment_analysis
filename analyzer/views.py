from django.shortcuts import render
from django.views.generic import FormView, ListView
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import AnalysisForm
from .models import AnalysisResult
from .services import analyze_text
from .serializers import AnalysisResultSerializer


class IndexView(FormView):
    template_name = "analyzer/index.html"
    form_class = AnalysisForm
    success_url = "/"

    def form_valid(self, form):
        text = form.cleaned_data["text"]
        result = analyze_text(text)
        obj = AnalysisResult.objects.create(text=text, **result)
        return render(self.request, "analyzer/result.html", {"obj": obj})


class HistoryView(ListView):
    model = AnalysisResult
    template_name = "analyzer/history.html"
    context_object_name = "results"
    paginate_by = 20
    ordering = ["-created_at"]


class AnalyzeAPIView(APIView):
    def post(self, request):
        text = request.data.get("text", "")
        if not text:
            return Response({"error": "text is required"}, status=400)

        result = analyze_text(text)
        obj = AnalysisResult.objects.create(text=text, **result)
        return Response(AnalysisResultSerializer(obj).data, status=201)