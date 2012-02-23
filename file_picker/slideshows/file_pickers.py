from django import forms
from django.core.files.base import ContentFile

import file_picker
from file_picker.slideshows.models import Slideshow

class SlideshowForm(forms.ModelForm):
    class Meta(object):
        model = Slideshow
        fields = ('name', 'description',)


class SlideshowPicker(file_picker.SlideshowPickerBase):
    form = SlideshowForm
    columns = ('name', 'date_modified')
    extra_headers = ('Name', 'Date modified')

file_picker.site.register(Slideshow, SlideshowPicker, name='slideshows')
