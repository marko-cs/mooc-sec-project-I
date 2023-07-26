from django import forms
from . import models

class AddURL(forms.ModelForm):
    class Meta:
        model = models.URLNotes
        fields = ['notes', 'url']
        exclude = ('user',)

