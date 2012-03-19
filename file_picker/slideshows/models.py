import os, datetime
from django.db import models
from file_picker.uploads.models import BaseMetaModel, Image

class Slideshow(BaseMetaModel):
    images = models.ManyToManyField(Image, through='SlideshowOrdering')

    class Meta:
        ordering = ('-date_modified',)

    def __unicode__(self):
        return self.name


class SlideshowOrdering(models.Model):
    slideshow = models.ForeignKey(Slideshow)
    image = models.ForeignKey(Image)
    sort_value = models.IntegerField()

    class Meta:
        ordering = ('sort_value',)

    def __unicode__(self):
        return self.slideshow.name


