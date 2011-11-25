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
    "Basic audio model. Includes AAC, OGG and WEBM references for best HTML5 playback potential"
    mp3_size = models.PositiveIntegerField(editable=False, null=True, blank=True)
    ogg_size = models.PositiveIntegerField(editable=False, null=True, blank=True)
    webm_size = models.PositiveIntegerField(editable=False, null=True, blank=True)
    mp3 = models.FileField(upload_to='uploads/audio/mp3/', null=False, blank=False, verbose_name="MP3 encoded audio file", help_text=_("Must be encoded as MP3 to play back correctly"))
    ogg = models.FileField(upload_to='uploads/audio/ogg/', null=False, blank=False, verbose_name="Ogg theora encoded audio file", help_text=_("Must be encoded as Ogg Theora to play back correctly"))
    webm = models.FileField(upload_to='uploads/audio/webm/', null=False, blank=False, verbose_name="WEBM encoded audio file", help_text=_("Must be encoded as WebM to play back correctly"))
    poster = models.ForeignKey(Image)
    is_podcast = models.BooleanField(default=False, blank=False)

    def save(self, *args, **kwargs):
        # file size
        if self.mp3 and self.ogg and self.webm:
            try:
                self.mp3_size = self.mp3.size
                self.ogg_size = self.ogg.size
                self.webm_size = self.webm.size
            except OSError:
                pass

        # make sure that both formats were specified or a video_url was provided"
        if self.mp3 and self.ogg and self.webm:
            super(Audio, self).save(*args, **kwargs)
        else:
            raise ValidationError("You must upload all audio types")


class Video(BaseMetaModel):
    "Basic video model. Includes both H.264 and OGG references for best HTML5 playback potential"
    h264_size = models.PositiveIntegerField(editable=False, null=True, blank=True)
    ogg_size = models.PositiveIntegerField(editable=False, null=True, blank=True)
    webm_size = models.PositiveIntegerField(editable=False, null=True, blank=True)
    h264 = models.FileField(upload_to='uploads/videos/h264/', null=True, blank=True, verbose_name="H.264 encoded video", help_text=_("Must be encoded as H.264 to play back correctly"))
    ogg = models.FileField(upload_to='uploads/videos/ogg/', null=True, blank=True, verbose_name="Ogg theora encoded video", help_text=_("Must be encoded as Ogg Theora to play back correctly"))
    webm = models.FileField(upload_to='uploads/videos/webm/', null=True, blank=True, verbose_name="WEBM encoded video", help_text=_("Must be encoded as WebM to play back correctly"))
    youtube_url = models.CharField(max_length=100, null=True, blank=True, verbose_name="YouTube URL", help_text=_("The full YouTube URL. Ex. http://www.youtube.com/watch?v=cmVLYaxHnPA"))
    poster = models.ForeignKey(Image)

    def save(self, *args, **kwargs):
        # file size
        if self.h264 and self.ogg and self.webm:
            try:
                self.h264_size = self.h264.size
                self.ogg_size = self.ogg.size
                self.webm_size = self.webm.size
            except OSError:
                pass

        # make sure that both formats were specified or a video_url was provided"
        if (self.h264 and self.ogg and self.webm) or self.youtube_url:
            super(Video, self).save(*args, **kwargs)
        else:
            raise ValidationError("You must upload all video types (H.264, Ogg and WEBM) or provide a YouTube URL")
