from django import forms


class FilePickerWidget(forms.Textarea):
    """ Base file picker widget that can be extended """

    def __init__(self, pickers, *args, **kwargs):
        self.pickers = pickers
        classes = kwargs.pop('classes', ['filepicker'])
        super(FilePickerWidget, self).__init__(*args, **kwargs)
        if 'file' in pickers:
            classes.append("file_picker_name_file_%s" % pickers['file'])
        if 'image' in pickers:
            classes.append("file_picker_name_image_%s" % pickers['image'])
        if 'audio' in pickers:
            classes.append("file_picker_name_audio_%s" % pickers['audio'])
        if 'video' in pickers:
            classes.append("file_picker_name_video_%s" % pickers['video'])
        if 'youtube' in pickers:
            classes.append("file_picker_name_youtube_%s" % pickers['youtube'])

        self.attrs['class'] = ' '.join(classes)


class SimpleFilePickerWidget(FilePickerWidget):
    """ Basic widget that provides Image/File links """

    def __init__(self, pickers, *args, **kwargs):
        kwargs['classes'] = ['simple-filepicker']
        super(SimpleFilePickerWidget, self).__init__(pickers, *args, **kwargs)

    class Media:
        css = {"all": ("file_picker/css/filepicker.overlay.css",)}
        js = ("file_picker/js/ajaxupload.js",
              "file_picker/js/jquery.filepicker.js",
              "file_picker/js/jquery.filepicker.simple.js")
