import os

from django import forms
from file_picker.exceptions import EmbedlyException
from file_picker.utils import get_embed_object

class VideoAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(VideoAdminForm, self).clean()

        file = cleaned_data.get('file')
        embed_url = cleaned_data.get('embed_url')

        if not file and not embed_url:
            raise forms.ValidationError("You must upload a file or provide an embed URL")

        if embed_url:
            try:
                cleaned_data['embed_object'] = get_embed_object(embed_url)
            except EmbedlyException, e:
                raise forms.ValidationError(str(e))

        return cleaned_data
