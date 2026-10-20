from django.shortcuts import render
from django.views.generic import FormView, ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .forms import AnalysisForm
from .models import AnalysisResult
from .services import analyze_text
from .serializers import AnalysisResultSerializer, AnalyzeRequestSerializer


class IndexView(FormView):
    template_name = "analyzer/index.html"
    form_class = AnalysisForm
    success_url = "/"

    def form_valid(self, form):
        text = form.cleaned_data["text"]
        try:
            result = analyze_text(text)
            obj = AnalysisResult.objects.create(text=text, **result)
            return render(self.request, "analyzer/result.html", {"obj": obj})
        except Exception as e:

            form.add_error(None, f"Analysis failed: {str(e)}")
            return self.form_invalid(form)


class HistoryView(ListView):
    model = AnalysisResult
    template_name = "analyzer/history.html"
    context_object_name = "results"
    paginate_by = 20
    ordering = ["-created_at"]


class AnalyzeAPIView(APIView):
    def post(self, request):

        serializer = AnalyzeRequestSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data["text"]

        try:

            result = analyze_text(text)
            obj = AnalysisResult.objects.create(text=text, **result)

            return Response(AnalysisResultSerializer(obj).data, status=status.HTTP_201_CREATED)

        except Exception as e:

            return Response(
                {"error": "Model inference failed. Please try again later.", "details": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )