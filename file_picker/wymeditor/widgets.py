from django.conf import settings
from file_picker.widgets import FilePickerWidget

class WYMeditorWidget(FilePickerWidget):
    def __init__(self, pickers, *args, **kwargs):
        kwargs['classes'] = ['wymeditor']
        super(WYMeditorWidget, self).__init__(pickers, *args, **kwargs)

    class Media:
        css = {'all': ('file_picker/css/filepicker.overlay.css',
                       'mediaelement/mediaelementplayer.min.css',)}
        js = (
            getattr(settings, 'JQUERY_URL',
            'https://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js'),
            'wymeditor/jquery.wymeditor.js',
            'wymeditor/jquery.wymeditor.filepicker.js',
            'wymeditor/plugins/embed/jquery.wymeditor.embed.js',
            'file_picker/js/ajaxupload.js',
            'file_picker/js/jquery.filepicker.js',
            'mediaelement/mediaelement-and-player.min.js',
        )
