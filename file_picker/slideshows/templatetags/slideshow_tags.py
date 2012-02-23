import re
import file_picker.settings as settings
from django import template as dj_template
from file_picker.slideshows.models import Slideshow

register = dj_template.Library()

@register.filter
def render_slideshows(content, template='slideshow/slideshow.html'):
    # parse out all slideshow tags
    regex = r'%s(?P<module_name>[a-zA-Z]+):(?P<slideshow_id>\d+)%s' % \
            (re.escape(settings.MODULE_TAG_BEGINS_WITH), re.escape(settings.MODULE_TAG_ENDS_WITH))
    tags = re.findall(regex, content)

    # replace tags with slideshow markup
    for tag in tags:
        module_name = tag[0]
        slideshow_id = tag[1]

        if module_name == 'slideshow':
            slideshow = Slideshow.objects.get(id=int(slideshow_id))

            # replace those tags with rendered slideshows
            ctx = { 'slideshow': slideshow }
            tpl = dj_template.loader.select_template([template])
            rendered_slideshow = tpl.render(dj_template.Context(ctx))
            tag = '%sslideshow:%s%s' % (settings.MODULE_TAG_BEGINS_WITH, slideshow_id, settings.MODULE_TAG_ENDS_WITH)
            content = content.replace(tag, rendered_slideshow)

    return content

render_slideshows.is_safe = True
