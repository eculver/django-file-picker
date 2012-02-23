from django.contrib import admin
from file_picker.slideshows.models import Slideshow

class SlideshowAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'caption', 'images',)

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


admin.site.register(Slideshow, SlideshowAdmin)
