from django.contrib import admin
from file_picker.uploads import models as upload_models

class UploadAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'file',)

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)

        # set created by only if it's new
        if not change:
            instance.created_by = request.user

        # always set modified by
        instance.modified_by = request.user

        # save instance and related fields
        instance.save()
        form.save_m2m()

        return instance


class AudioUploadAdmin(UploadAdmin):
    list_display = ('name', 'is_podcast',)
    fields = ('name', 'description', 'file', 'poster', 'is_podcast',)


class VideoUploadAdmin(UploadAdmin):
    fields = ('name', 'description', 'file', 'youtube_url', 'poster',)

admin.site.register(upload_models.File, UploadAdmin)
admin.site.register(upload_models.Image, UploadAdmin)
admin.site.register(upload_models.Audio, AudioUploadAdmin)
admin.site.register(upload_models.Video, VideoUploadAdmin)
