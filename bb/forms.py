from __future__ import unicode_literals
from django import forms
from DjangoUeditor.forms import UEditorWidget


class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class TopicUEditorForm(forms.Form):
    Name = forms.CharField(label=u'topic title')
    Content = forms.CharField(label=u'content',
                              widget=UEditorWidget({'width': 600, 'height': 500, 'imagePath': 'images/',
                                                    'filePath': 'files/'})
                              )


class PostReplyForm(forms.Form):
    Content = forms.CharField(
                              widget=UEditorWidget({'width': 600, 'height': 300, 'imagePath': 'images/',
                                                    'filePath': 'files/'})
                              )