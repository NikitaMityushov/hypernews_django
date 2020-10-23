from django import forms
from datetime import datetime


class PostNewsForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        tl = self.cleaned_data.get('title')
        return tl

    def clean_text(self):
        tx = self.cleaned_data.get('text')
        return tx

    def save(self):
        created = str(datetime.now())[:-7]
        text = self.cleaned_data.get('text')
        title = self.cleaned_data.get('title')
        return {"created": created, "text": text, "title": title}
