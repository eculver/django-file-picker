from django import forms
from django.contrib import admin
from django.db import models
from sample_project.article.models import Post

import file_picker


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        from file_picker.widgets import SimpleFilePickerWidget
        from file_picker.wymeditor.widgets import WYMeditorWidget
        pickers = {'file': "files", 'image': "images", 'audio': "audio", 'video': "videos"}
        # simple widget
        simple_widget = SimpleFilePickerWidget(pickers=pickers)
        self.fields['body'].widget = simple_widget
        # wymeditor widget
        wym_widget = WYMeditorWidget(pickers=pickers)
        self.fields['teaser'].widget = wym_widget

    class Meta(object):
        model = Post


class PostAdmin(admin.ModelAdmin):
    form = PostForm

admin.site.register(Post, PostAdmin)

