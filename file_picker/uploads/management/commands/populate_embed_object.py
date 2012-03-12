import file_picker.settings as settings

from django.core.management.base import BaseCommand, CommandError
from file_picker.exceptions import EmbedlyException
from file_picker.utils import get_embed_object
from file_picker.uploads.models import Video

class Command(BaseCommand):
    help = 'Populates the `embed_object` field of Video model\
            from previous url fields (youtube, etc.) in order\
            to provide a way to migrate from pre-embed supported versions.'

    def handle(self, *args, **options):
        num_updated = 0
        videos = Video.objects.all()

        for video in videos:
            if video.embed_url and not video.embed_object:
                print "Trying to update '%s'..." % video.name
                try:
                    video.embed_object = get_embed_object(video.embed_url)

                    if video.embed_object:
                        video.save()
                        num_updated = num_updated + 1
                        print "Successfully updated '%s'" % video.name
                    else:
                        print "Couldn't update '%s': No object returned" % video.name
                except EmbedlyException, e:
                    print "Couldn't update '%s': %s" % (video.name, str(e),)

        print "Updated %d video instances" % num_updated



