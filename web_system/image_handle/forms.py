# image_handle/forms.py
from django import forms

class AnalysisForm(forms.Form):
    text_content = forms.CharField(widget=forms.Textarea, max_length=1000)