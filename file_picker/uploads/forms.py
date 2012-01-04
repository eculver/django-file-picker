import os

from django import forms
from django.db import models
from django.db.models import Q, get_model
from django.db.models.base import FieldDoesNotExist

from django.core.files.base import ContentFile


class VideoAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(VideoAdminForm, self).clean()

        file = cleaned_data.get('file')
        youtube_url = cleaned_data.get('youtube_url')

        if not file and not youtube_url:
            raise forms.ValidationError("You must upload a file or provide a YouTube URL")

        return cleaned_data
