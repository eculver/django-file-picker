from django.conf import settings

NOT_FOUND_STRING = getattr(settings, 'FILE_PICKER_NOT_FOUND_STRING', 'Not Found')
THUMBNAIL_SIZE = getattr(settings, 'FILE_PICKER_THUMBNAIL_SIZE', '100x100')
MEDIA_URL = getattr(settings, 'FILE_PICKER_MEDIA_URL', settings.MEDIA_URL)
STATIC_URL = getattr(settings, 'FILE_PICKER_STATIC_URL', settings.STATIC_URL)
MODULE_TAG_BEGINS_WITH = getattr(settings, 'FILE_PICKER_MODULE_TAG_BEGINS_WITH', '[[')
MODULE_TAG_ENDS_WITH = getattr(settings, 'FILE_PICKER_MODULE_TAG_ENDS_WITH', ']]')
EMBEDLY_KEY = getattr(settings, 'FILE_PICKER_EMBEDLY_KEY', None)
EMBED_MAX_WIDTH = getattr(settings, 'FILE_PICKER_EMBED_MAX_WIDTH', '')
EMBED_MAX_HEIGHT = getattr(settings, 'FILE_PICKER_EMBED_MAX_HEIGHT', '')
