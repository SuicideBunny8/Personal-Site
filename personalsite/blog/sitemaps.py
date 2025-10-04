from django.contrib.sitemaps import Sitemap
from .models import Post, Tag

class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.7 # default

    def items(self):
        return Post.objects.filter(draft=False)

    def lastmod(self, post):
        return post.pub_date