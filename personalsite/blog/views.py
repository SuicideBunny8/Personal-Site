from django.views.generic import TemplateView, DetailView, ListView
from .models import Post

# Create your views here.
class HomeView(ListView):
    template_name = "blog/home.html"
    model = Post
    ordering = "-pub_date"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add stuff
        context["featured_posts"] = self.get_queryset().filter(featured=True)#.filer(draft=False) # remove draft for testing
        context["recent_posts"] = self.get_queryset().filter(draft=False)[:5]
        return context

class PostView(DetailView):
    template_name = "blog/post_detail.html"
    model = Post

class PostListView(ListView):
    template_name = "blog/post_list.html"
    model = Post
    ordering = "-pub_date"
    context_object_name = "posts"