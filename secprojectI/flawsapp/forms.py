""" Form definition to add new url into db"""
from django import forms
from . import models

class AddURL(forms.ModelForm):
    """ Form to add new URL and related notes """
    class Meta:
        model = models.URLNotes
        fields = ["notes", "url"]
        #exclude = ("user",)
