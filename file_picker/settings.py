from django.conf import settings

NOT_FOUND_STRING = getattr(settings, 'FILE_PICKER_NOT_FOUND_STRING', 'Not Found')
MEDIA_URL = getattr(settings, 'FILE_PICKER_MEDIA_URL', settings.MEDIA_URL)
STATIC_URL = getattr(settings, 'FILE_PICKER_STATIC_URL', settings.STATIC_URL)
