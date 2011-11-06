from file_picker.settings import STATIC_URL
from file_picker.widgets import FilePickerWidget


class WYMeditorWidget(FilePickerWidget):
    def __init__(self, pickers, *args, **kwargs):
        kwargs['classes'] = ['wymeditor']
        super(WYMeditorWidget, self).__init__(pickers, *args, **kwargs)

    class Media:
        css = {"all": ("%s/css/filepicker.overlay.css" % STATIC_URL,)}
        js = ("%s/wymeditor/jquery.wymeditor.js" % STATIC_URL,
              "%s/js/ajaxupload.js" % STATIC_URL,
              "%s/js/jquery.filepicker.js" % STATIC_URL,
              "%s/js/jquery.wymeditor.filepicker.js" % STATIC_URL)
