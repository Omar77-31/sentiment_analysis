import re
from django import forms


class AnalysisForm(forms.Form):
    text = forms.CharField(
        label="Text",
        max_length=2000,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Enter a review, comment, or tweet...",
        }),
    )

    def clean_text(self):
        text = self.cleaned_data["text"]

        if not re.search(r'[\u0600-\u06FF]', text):
            raise forms.ValidationError("Please enter valid Arabic text. (الرجاء إدخال نص عربي صالح)")
        return text