import os

from django import forms

from embedly import Embedly

class VideoAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(VideoAdminForm, self).clean()

        file = cleaned_data.get('file')
        embed_url = cleaned_data.get('embed_url')

        if not file and not embed_url:
            raise forms.ValidationError("You must upload a file or provide an embed URL")

        if embed_url:
            cleaned_data['embed_object'] = get_embed_object(embed_url)

        return cleaned_data
