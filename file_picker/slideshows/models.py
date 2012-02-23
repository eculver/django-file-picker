import os, datetime
from django.db import models
from sortedm2m.fields import SortedManyToManyField
from file_picker.uploads.models import BaseMetaModel, Image

class Slideshow(BaseMetaModel):
    images = SortedManyToManyField(Image)

    class Meta:
        ordering = ('-date_modified',)

    def __unicode__(self):
        return self.name


