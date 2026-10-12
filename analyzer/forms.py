from django import forms


class AnalysisForm(forms.Form):
    text = forms.CharField(
        label="Text",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Enter a review, comment, or tweet...",
        }),
    )