from django import forms
from django.core.files.base import ContentFile

import file_picker
from file_picker.exceptions import EmbedlyException
from file_picker.utils import get_embed_object
from file_picker.uploads.models import File, Image, Audio, Video


class FileForm(forms.ModelForm):
    file = forms.CharField(widget=forms.widgets.HiddenInput())

    class Meta(object):
        model = File
        fields = ('name', 'description', 'caption',)

    def save(self, commit=True):
        form = super(FileForm, self).save(commit=False)
        file_path = self.cleaned_data['file']
        fh = ContentFile(open(self.cleaned_data['file'], 'r').read())
        form.file.save(file_path, fh)
        if commit:
            form.save()
        return form


class ImageForm(forms.ModelForm):
    file = forms.CharField(widget=forms.widgets.HiddenInput())

    class Meta(object):
        model = Image
        fields = ('name', 'description', 'caption',)

    def save(self, commit=True):
        form = super(ImageForm, self).save(commit=False)
        file_path = self.cleaned_data['file']
        fh = ContentFile(open(self.cleaned_data['file'], 'r').read())
        form.file.save(file_path, fh)
        if commit:
            form.save()
        return form


class AudioForm(forms.ModelForm):
    file = forms.CharField(widget=forms.widgets.HiddenInput())

    class Meta(object):
        model = Audio
        fields = ('name', 'description', 'caption', 'poster',)

    def save(self, commit=True):
        form = super(AudioForm, self).save(commit=False)
        file_path = self.cleaned_data['file']
        fh = ContentFile(open(self.cleaned_data['file'], 'r').read())
        form.file.save(file_path, fh)
        if commit:
            form.save()
        return form


class VideoForm(forms.ModelForm):
    file = forms.CharField(widget=forms.widgets.HiddenInput())

    class Meta(object):
        model = Video
        fields = ('name', 'description', 'caption', 'poster', 'embed_url',)

    def clean(self):
        cleaned_data = super(VideoForm, self).clean()

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

    def save(self, commit=True):
        video = super(VideoForm, self).save(commit=False)
        video.embed_object = self.cleaned_data['embed_object']
        file_path = self.cleaned_data['file']

        if file_path and file_path != 'none':
            fh = ContentFile(open(self.cleaned_data['file'], 'r').read())
            video.file.save(file_path, fh)

        if commit:
            video.save()

        return video


class FilePicker(file_picker.FilePickerBase):
    form = FileForm
    columns = ('name', 'file_type', 'date_modified')
    extra_headers = ('Name', 'File type', 'Date modified')


class ImagePicker(file_picker.ImagePickerBase):
    form = ImageForm
    columns = ('name', 'file_type', 'date_modified')
    extra_headers = ('Name', 'File Type', 'Date Modified')


class AudioPicker(file_picker.AudioPickerBase):
    form = AudioForm
    columns = ('name', 'file_type', 'date_modified')
    extra_headers = ('Name', 'File Type', 'Date Modified')


class VideoPicker(file_picker.VideoPickerBase):
    form = VideoForm
    columns = ('name', 'file_type', 'embed_url', 'date_modified',)
    extra_headers = ('Name', 'File Type', 'URL', 'Date Modified',)


file_picker.site.register(File, FilePicker, name='files')
file_picker.site.register(Image, ImagePicker, name='images')
file_picker.site.register(Audio, AudioPicker, name='audio')
file_picker.site.register(Video, VideoPicker, name='videos')
