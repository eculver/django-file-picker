import mimetypes

from os.path import join
from django import template
from file_picker.parse import parse_types
from file_picker.settings import NOT_FOUND_STRING, MEDIA_URL

def render_upload(file, template_path="file_picker/render/", **options):
    """
    Render a single ``File`` or ``Image`` model instance using the
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
    if file is None:
        return NOT_FOUND_STRING

    template_name = options.pop('as', None)
    if template_name:
        templates = [template_name,
                     "%s/default" % template_name.split('/')[0],
                     "default"]
    else:
        [file_type, file_subtype] = parse_types(file.url)
        templates = [join(file_type, file_subtype),
                     join(file_type, "default"),
                     "default"]

    tpl = template.loader.select_template(
        ["%s.html" % join(template_path, p) for p in templates])

    return tpl.render(template.Context({'file': file,
                                        'media_url': MEDIA_URL,
                                        'options': options}))
