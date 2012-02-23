from django.conf.urls.defaults import *
from sample_project.article.views import PostView

urlpatterns = patterns('sample_project.article.views',
    url(r'(?P<post_id>\d+)/?$', PostView.as_view(), name='article_article'),
)
