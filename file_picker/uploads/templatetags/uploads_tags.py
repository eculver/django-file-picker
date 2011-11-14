from django import template

from file_picker.uploads.parse import parse_options
from file_picker.uploads import utils

register = template.Library()

@register.filter
def render_upload(upload, opts_str=''):
    """
    Render a single ``FileUpload`` model instance using the
    appropriate render template for its mime type.

    Expects options to be in the format "key=val:key2=val2", just like
    the embed syntax. Options are parsed into a dictionary and passed
    to ``render_upload``. (A ``template_path`` option can be passed
    and it will be used as the search path for rendering templates.)

    Just wraps ``adminfiles.utils.render_upload``.

    """
    return utils.render_upload(upload, **parse_options(opts_str))
render_upload.is_safe = True
