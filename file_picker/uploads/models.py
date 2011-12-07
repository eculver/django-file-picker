import os, datetime, mimetypes

from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from file_picker.parse import parse_types


class BaseMetaModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created",
                                   null=True, blank=True)
    modified_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modified",
                                    null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('-date_modified',)

    def __unicode__(self):
        return self.name


class BaseFileModel(BaseMetaModel):
    file_size = models.PositiveIntegerField(editable=False, null=True, blank=True)
    file_type = models.CharField(editable=False, max_length=16, blank=True)
    file_subtype = models.CharField(editable=False, max_length=16, blank=True)

    class Meta:
        abstract = True

    def save(self, **kwargs):
        # file size
        try:
            self.file_size = self.file.size
        except Exception:
            pass

        # file types from mimetype
        if self.file:
            [self.file_type, self.file_subtype] = parse_types(self.file.path)

        return super(BaseFileModel, self).save(**kwargs)


class File(BaseFileModel):
    "Basic file model"
    file = models.FileField(upload_to='uploads/files/', blank=False)


class Image(BaseFileModel):
    "Basic image model"
    file = models.ImageField(upload_to='uploads/images/', blank=False)


class Audio(BaseFileModel):
    "Basic audio model"
    file = models.FileField(upload_to='uploads/audio/', null=False, blank=False, verbose_name="MP3 encoded audio file", help_text=_("Must be encoded as MP3 to play back correctly"))
    poster = models.ForeignKey(Image)
    is_podcast = models.BooleanField(default=False, blank=False)

    class Meta:
        verbose_name = 'Audio'
        verbose_name_plural = 'Audio'


class Video(BaseFileModel):
    "Basic video model"
    file = models.FileField(upload_to='uploads/videos/', null=True, blank=True, verbose_name="H.264 encoded video", help_text=_("Must be encoded as H.264 to play back correctly"))
    youtube_url = models.CharField(max_length=100, null=True, blank=True, verbose_name="YouTube embed URL", help_text=_("The YouTube embed URL. Ex. http://www.youtube.com/embed/cmVLYaxHnPA"))
    poster = models.ForeignKey(Image)

    def save(self, *args, **kwargs):
        # make sure that a file was uploaded or a youtube_url was provided
        if self.file or self.youtube_url:
            super(Video, self).save(*args, **kwargs)
        else:
            raise ValidationError("You must a file or provide a YouTube URL")

