import os
import logging
import traceback
import tempfile
import datetime

import file_picker.settings as settings

from django.db import models
from django.db.models import Q
from django.utils import simplejson as json
from django.utils.text import capfirst
from django.http import HttpResponse, HttpResponseServerError
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import UploadedFile
from django.views.decorators.csrf import csrf_exempt

from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.helpers import ThumbnailError
from file_picker.forms import QueryForm, model_to_AjaxItemForm
from file_picker.utils import render_upload, render_youtube

logger = logging.getLogger('filepicker.views')


class FilePickerBase(object):
    model = None
    form = None
    page_size = 4
    link_headers = ['Insert File',]
    extra_headers = None
    columns = None
    ordering = None

    def __init__(self, name, model):
        self.name = name
        self.model = model
        if not self.form:
            self.form = model_to_AjaxItemForm(self.model)
        self.field_names = model._meta.get_all_field_names()
        field_names = model._meta.get_all_field_names()
        build_headers = not self.columns or not self.extra_headers
        if not self.columns:
            self.columns = self.field_names
        extra_headers = []

        for field_name in field_names:
            try:
                field = model._meta.get_field(field_name)
            except models.FieldDoesNotExist:
                self.field_names.remove(field_name)
                continue
            if isinstance(field, (models.ImageField, models.FileField)):
                self.field = field_name
                self.field_names.remove(field_name)
            elif isinstance(field, (models.ForeignKey, models.ManyToManyField)):
                self.field_names.remove(field_name)
        for field_name in self.columns:
            try:
                field = model._meta.get_field(field_name)
            except models.FieldDoesNotExist:
                self.field_names.remove(field_name)
                continue
            extra_headers.append(capfirst(field.verbose_name))
        if build_headers:
            self.extra_headers = extra_headers


    def protect(self, view, csrf_exempt=False):
        def wrapper(*args, **kwargs):
            data = {}
            try:
                return view(*args, **kwargs)
            except Exception, e:
                logger.exception(e)
                data['errors'] = [traceback.format_exc(e)]
            return HttpResponse(json.dumps(data), mimetype='application/json')
        wrapper.csrf_exempt = csrf_exempt
        return wrapper

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urlpatterns = patterns('',
            url(r'^$', self.setup, name='init'),
            url(r'^files/$', self.list, name='list-files'),
            url(r'^upload/file/$', self.protect(self.upload_file, True),
                name='upload-file'),
        )
        return (urlpatterns, None, self.name)
    urls = property(get_urls)
    
    def setup(self, request):
        data = {}
        data['urls'] = {
            'browse': {'files': reverse('filepicker:%s:list-files' % self.name)},
            'upload': {'file': reverse('filepicker:%s:upload-file' % self.name)},
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
    
    def append(self, obj):
        extra = {}
        for name in self.columns:
            value = getattr(obj, name)
            if isinstance(value, (datetime.datetime, datetime.date)):
                value = value.strftime('%b %d, %Y')
            else:
                value = unicode(value)
            extra[name] = value

        try:
            url = getattr(obj, self.field).url
        except:
            url = ''

        return {'name': unicode(obj), 'url': url,
            'extra': extra,
            'insert': [url,],
            'link_content': ['Click to insert'],
        }

    def get_queryset(self, search):
        qs = Q()
        if search:
            for name in self.field_names:
                comparision = {}
                comparision[name] = search
                qs = qs | Q(name__contains=search)
            queryset = self.model.objects.filter(qs)
        else:
            queryset = self.model.objects.all()
        if self.ordering:
            queryset = queryset.order_by(self.ordering)
        return queryset

    def upload_file(self, request):
        if 'userfile' in request.FILES:
            name, ext = os.path.splitext(request.FILES['userfile'].name)
            fn = tempfile.NamedTemporaryFile(prefix=name, suffix=ext, delete=False)
            f = request.FILES['userfile']
            for chunk in f.chunks():
                fn.write(chunk)
            fn.close()
            return HttpResponse(json.dumps({ 'name': fn.name }), mimetype='application/json')
        else:
            form = self.form(request.POST or None)
            if form.is_valid():
                obj = form.save()
                data = self.append(obj)
                return HttpResponse(json.dumps(data),
                                    mimetype='application/json')
            data = {'form': form.as_table()}
            return HttpResponse(json.dumps(data), mimetype='application/json')

    def list(self, request):
        form = QueryForm(request.GET)
        if not form.is_valid():
            return HttpResponseServerError()
        page = form.cleaned_data['page']
        result = []
        qs = self.get_queryset(form.cleaned_data['search'])
        pages = Paginator(qs, self.page_size)
        try:
            page_obj = pages.page(page)
        except EmptyPage:
            return HttpResponseServerError()
        for obj in page_obj.object_list:
            result.append(self.append(obj))

        data = {
            'page': page,
            'pages': pages.page_range,
            'search': form.cleaned_data['search'],
            'result': result,
            'model': self.model.__name__,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'link_headers': self.link_headers,
            'extra_headers': self.extra_headers,
            'columns': self.columns,
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')


class ImagePickerBase(FilePickerBase):
    link_headers = ['Thumbnail',]

    def append(self, obj):
        json = super(ImagePickerBase, self).append(obj)
        instance = getattr(obj, self.field)

        try:
            thumb = get_thumbnail(instance, settings.THUMBNAIL_SIZE)
        except ThumbnailError, e:
            logger.exception(e)
            thumb = None

        if thumb:
            thumb_formatted = ['<img src=\'%s\'>' % thumb.url,]
            image_formatted = [render_upload(obj),]
            json['link_content'] = thumb_formatted
            json['insert'] = image_formatted
        else:
            json['link_content'] = [settings.NOT_FOUND_STRING,]
            json['insert'] = [settings.NOT_FOUND_STRING,]

        return json


class AudioPickerBase(FilePickerBase):
    link_headers = ['Audio File',]
    poster_field = 'poster'

    def append(self, obj):
        json = super(AudioPickerBase, self).append(obj)
        instance = getattr(obj, self.field)

        audio_formatted = [render_upload(obj),]
        json['link_content'] = ['Click to insert'];
        json['poster'] = obj.poster.file.url
        json['insert'] = audio_formatted

        return json


class VideoPickerBase(FilePickerBase):
    link_headers = ['Video File',]
    poster_field = 'poster'

    def append(self, obj):
        json = super(VideoPickerBase, self).append(obj)
        instance = getattr(obj, self.field)

        if obj.embed_object:
            # try to grab and decode the embed object
            video_formatted = [obj.embed_object]
        elif obj.file:
            video_formatted = [render_upload(obj)]
        else:
            video_formatted = ['unknown']

        json['link_content'] = ['Click to insert'];
        json['insert'] = video_formatted
        json['poster'] = poster = obj.poster.file.url

        return json


class SlideshowPickerBase(FilePickerBase):
    field = 'images'
    link_headers = ['Slideshow',]

    def append(self, obj):
        json = super(SlideshowPickerBase, self).append(obj)

        try:
            first_image = obj.images.all()[0]
        except Exception, e:
            first_image = None

        try:
            thumb = get_thumbnail(first_image.file, settings.THUMBNAIL_SIZE)
            thumb_formatted = '<img src=\'%s\'>' % thumb.url
        except ThumbnailError, e:
            logger.exception(e)
            thumb = None
            thumb_formatted = settings.NOT_FOUND_STRING

        slideshow_tag = '%sslideshow:%d%s' % (settings.MODULE_TAG_BEGINS_WITH,\
                                              obj.pk,\
                                              settings.MODULE_TAG_ENDS_WITH)

        # generate the insert link
        json['link_content'] = [thumb_formatted,]
        json['insert'] = [slideshow_tag,]

        return json


