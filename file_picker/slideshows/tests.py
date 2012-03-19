from django.contrib.auth.models import User
from django.test import TestCase

from file_picker.uploads.models import Image
from file_picker.slideshows.models import Slideshow
from file_picker.slideshows.templatetags.slideshow_tags import render_slideshows

class TemplateTagsTestCase(TestCase):
    def setUp(self):
        self.content_single = u'Lorem ipsum dolor sit amet, consectetur adipisicing elit [[slideshow:1]]'
        self.content_multi = u'[[slideshow:2]] Lorem ipsum dolor sit amet, consectetur adipisicing elit [[slideshow:1]]'

        slideshow_1 = self.new_slideshow('test slideshow', 'test desc', 'test caption')
        slideshow_2 = self.new_slideshow('test slideshow', 'test desc', 'test caption')

        image_1 = self.new_image('test image 1', 'test desc', 'test caption')
        image_1.slideshow = slideshow_1
        image_1.save()
        image_1.slideshow = slideshow_2

        image_2 = self.new_image('test image 2', 'test desc', 'test caption')
        image_2.slideshow = slideshow_2
        image_2.save()
        image_2.slideshow = slideshow_2

    def new_image(self, name, description, caption, **kwargs):
        i = Image(name=name, description=description, caption=caption, **kwargs)
        i.save()
        return i


    def new_slideshow(self, name, description, caption, **kwargs):
        ss = Slideshow(name=name, description=description, caption=caption, **kwargs)
        ss.save()
        return ss


    def test_single_replace(self):
        """Test replacing of a single slideshow tag"""

        new_content = render_slideshows(self.content_single, template='slideshows/slideshow_test.html')
        expected_content = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit test test test\n'

        self.assertEqual(str(new_content), expected_content)

    def test_multi_replace(self):
        """Test replacing of multiple slideshow tags"""

        new_content = render_slideshows
        new_content = render_slideshows(self.content_multi, template='slideshows/slideshow_test.html')
        expected_content = 'test test test\nLorem ipsum dolor sit amet, consectetur adipisicing elit test test test\n'






