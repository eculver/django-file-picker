from django import forms
from django.core.files.base import ContentFile

import file_picker
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
        fields = ('name', 'description', 'caption', 'poster', 'youtube_url',)

    def save(self, commit=True):
        form = super(VideoForm, self).save(commit=False)
        file_path = self.cleaned_data['file']
        fh = ContentFile(open(self.cleaned_data['file'], 'r').read())
        form.file.save(file_path, fh)
        if commit:
            form.save()
        return form


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
    columns = ('name', 'file_type', 'youtube_url', 'date_modified',)
    extra_headers = ('Name', 'File Type', 'YouTube URL', 'Date Modified',)


file_picker.site.register(File, FilePicker, name='files')
file_picker.site.register(Image, ImagePicker, name='images')
file_picker.site.register(Audio, AudioPicker, name='audio')
file_picker.site.register(Video, VideoPicker, name='videos')
