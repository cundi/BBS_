from django import forms
from .models import Topic


class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class PageForm(forms.ModelForm):
    class Meta:
        model = Topic