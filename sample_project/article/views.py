from django.views.generic.base import View
from django.template import RequestContext
from django.shortcuts import render_to_response as r_t_r
from django.shortcuts import get_object_or_404
from sample_project.article.models import Post

# Shortcut used to always call render_to_response with a context_instance
render_to_response = lambda r, t, c: r_t_r(t, c, context_instance=RequestContext(r))

class PostView(View):
    "Post view"
    template_name = 'article/post.html'

    def dispatch(self, request, post_id):
        self.post = get_object_or_404(Post, id=post_id)
        return render_to_response(request, self.template_name, self.context(request))

    def context(self, request):
        return {
            'post': self.post
        }

