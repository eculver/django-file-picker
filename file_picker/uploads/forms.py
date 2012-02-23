import os
import file_picker.settings as settings

from django import forms
from django.core.exceptions import ImproperlyConfigured

from embedly import Embedly

class VideoAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(VideoAdminForm, self).clean()

        file = cleaned_data.get('file')
        embed_url = cleaned_data.get('embed_url')

        if not file and not embed_url:
            raise forms.ValidationError("You must upload a file or provide a YouTube URL")

        if embed_url:
            # try to look up embed data from Embedly
            if not settings.EMBEDLY_KEY:
                raise ImproperlyConfigured("You have not specified an Embedly key in your settings file.")

            try:
                client = Embedly(settings.EMBEDLY_KEY)
                if client.is_supported(embed_url):
                    resp = client.oembed(embed_url, maxwidth=settings.EMBED_MAX_WIDTH, maxheight=settings.EMBED_MAX_HEIGHT)
                else:
                    raise forms.ValidationError("The provider for the URL you provided is not supported by Embed.ly. Please try again.")
            except Exception, e:
                raise forms.ValidationError("There was an issue with your embed URL. Please check that it is valid and try again")

            if resp.error:
                print settings.EMBEDLY_KEY
                raise forms.ValidationError("There was an issue looking up your embed URL: %s:%s" % (resp.error_code, resp.error_message))

            cleaned_data['embed_object'] = resp['html']

        return cleaned_data
