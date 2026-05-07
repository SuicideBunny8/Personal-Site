from django.views.generic import TemplateView, DetailView, ListView
from .models import Post, PostStatus

# Create your views here.
class HomeView(ListView):
    template_name = "blog/home.html"
    model = Post
    ordering = "-pub_date"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add stuff
        context["featured_posts"] = self.get_queryset().filter(status=PostStatus.FEATURED)
        context["recent_posts"] = self.get_queryset().filter(draft=False)[:5]
        return context

class PostView(DetailView):
    template_name = "blog/post_detail.html"
    model = Post

class PostListView(ListView):
    queryset = Post.objects.filter(status=PostStatus.PUBLISHED)
    paginate_by = 10
    template_name = "blog/post_list.html"
    model = Post
    ordering = "-pub_date"
    context_object_name = "posts"