from django.contrib.sitemaps import Sitemap
from django.db.models import Q
from .models import Post, PostStatus, Tag

class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.7 # default

    def items(self):
        return Post.objects.filter(Q(status=PostStatus.PUBLISHED) | Q(status=PostStatus.FEATURED))

    def lastmod(self, post):
        return post.pub_date