from django import forms
from django.db.models import get_model
from sample_project.blog.widgets import WYMEditor

class ImageForm(forms.Form):
    pass
    
class PostAdminModelForm(forms.ModelForm):
    body = forms.CharField(widget=WYMEditor())

    class Meta:
        model = get_model('blog', 'post')
