import mimetypes
import file_picker.settings as settings

from os.path import join
from embedly import Embedly
from django import template
from django.core.exceptions import ImproperlyConfigured
from file_picker.exceptions import EmbedlyException
from file_picker.parse import parse_types

def render_upload(obj, template_path="file_picker/render/", **options):
    """
    Render a single ``File`` or ``Image`` model instance (``obj``) using the
    appropriate rendering template and the given keyword options, and
    return the rendered HTML.

    The template used to render each upload is selected based on the
    mime-type of the upload. For an upload with mime-type
    "image/jpeg", assuming the default ``template_path`` of
    "file_picker/render", the template used would be the first one
    found of the following: ``file_picker/render/image/jpeg.html``,
    ``file_picker/render/image/default.html``, and
    ``file_picker/render/default.html``

    """
    if obj is None or obj.file is None:
        return settings.NOT_FOUND_STRING

    template_name = options.pop('as', None)

    if template_name:
        templates = [template_name,
                     "%s/default" % template_name.split('/')[0],
                     "default"]
    else:
        [file_type, file_subtype] = parse_types(obj.file.url)
        templates = [join(file_type, file_subtype),
                     join(file_type, "default"),
                     "default"]

    tpl = template.loader.select_template(
        ["%s.html" % join(template_path, p) for p in templates])

    return tpl.render(template.Context({'obj': obj,
                                        'media_url': settings.MEDIA_URL,
                                        'options': options}))

def render_youtube(obj, template_path="file_picker/render/", **options):
    """
    Render a single ``Video`` model instance using the
    appropriate youtube rendering template and the given keyword options, and
    return the rendered HTML.

    """
    if obj is None or obj.file is None:
        return NOT_FOUND_STRING

    templates = ['video/youtube']

    tpl = template.loader.select_template(
        ["%s.html" % join(template_path, p) for p in templates])

    return tpl.render(template.Context({'obj': obj,
                                        'media_url': MEDIA_URL,
                                        'options': options}))

def get_embed_object(url):
    if not settings.EMBEDLY_KEY:
        raise ImproperlyConfigured("You have not specified an Embedly key in your settings file.")

    try:
        client = Embedly(settings.EMBEDLY_KEY)
        resp = client.oembed(url, maxwidth=settings.EMBED_MAX_WIDTH, maxheight=settings.EMBED_MAX_HEIGHT)
    except Exception, e:
        raise EmbedlyException("There was an issue with your embed URL. Please check that it is valid and try again")


    if resp.error:
        raise EmbedlyException("There was an issue looking up your embed URL: %s:%s" % (resp.error_code, resp.error_message))

    if not resp.get('html'):
        raise EmbedlyException("There was an issue looking up your embed URL: The provider is not supported by Embedly.")

    return resp.get('html')
