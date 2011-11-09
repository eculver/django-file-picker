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
        except OSError:
            pass

        # file types from mimetype
        [self.file_type, self.file_subtype] = parse_types(self.file.path)

        return super(BaseFileModel, self).save(**kwargs)


class File(BaseFileModel):
    "Basic file model"
    file = models.FileField(upload_to='uploads/files/')


class Image(BaseFileModel):
    "Basic image model"
    file = models.ImageField(upload_to='uploads/images/')


class Audio(BaseMetaModel):
    "Basic audio model. Includes both AAC and OGG references for best HTML5 playback potential"
    aac_size = models.PositiveIntegerField(editable=False, null=True, blank=True)
    ogg_size = models.PositiveIntegerField(editable=False, null=True, blank=True)
    aac = models.FileField(upload_to='uploads/audio/aac/', null=False, blank=False, verbose_name="AAC or MP3 encoded audio file", help_text=_("Must be encoded in AAC or MP3 to play back correctly"))
    ogg = models.FileField(upload_to='uploads/audio/ogg/', null=False, blank=False, verbose_name="Ogg theora encoded audio file", help_text=_("Must be encoded in Ogg Theora to play back correctly"))
    poster = models.ForeignKey(Image)
    is_podcast = models.BooleanField(default=False, blank=False)

    def save(self, *args, **kwargs):
        # file size
        if self.aac and self.ogg:
            try:
                self.aac_size = self.aac.size
                self.ogg_size = self.ogg.size
            except OSError:
                pass

        # make sure that both formats were specified or a video_url was provided"
        if self.aac and self.ogg:
            super(Audio, self).save(*args, **kwargs)
        else:
            raise ValidationError("You must upload both audio types")


class Video(BaseMetaModel):
    "Basic video model. Includes both H.264 and OGG references for best HTML5 playback potential"
    h264_size = models.PositiveIntegerField(editable=False, null=True, blank=True)
    ogg_size = models.PositiveIntegerField(editable=False, null=True, blank=True)
    h264 = models.FileField(upload_to='uploads/videos/h264/', null=True, blank=True, verbose_name="H.264 encoded video", help_text=_("Must be encoded in H.264 to play back correctly"))
    ogg = models.FileField(upload_to='uploads/videos/ogg/', null=True, blank=True, verbose_name="Ogg theora encoded video", help_text=_("Must be encoded in Ogg Theora to play back correctly"))
    youtube_url = models.CharField(max_length=100, null=True, blank=True, verbose_name="YouTube URL", help_text=_("The full YouTube URL. Ex. http://www.youtube.com/watch?v=cmVLYaxHnPA"))
    poster = models.ForeignKey(Image)

    def save(self, *args, **kwargs):
        # file size
        if self.h264 and self.ogg:
            try:
                self.h264_size = self.h264.size
                self.ogg_size = self.ogg.size
            except OSError:
                pass

        # make sure that both formats were specified or a video_url was provided"
        if (self.h264 and self.ogg) or self.youtube_url:
            super(Video, self).save(*args, **kwargs)
        else:
            raise ValidationError("You must upload both video types (H.264 & Ogg) or provide a video_url")
