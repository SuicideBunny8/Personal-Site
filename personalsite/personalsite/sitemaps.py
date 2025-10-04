from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.sitemaps import PostSitemap


class RootSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return [
            'homepage',
            'post_list_view',
            'about'
        ]

    def location(self, item):
        return reverse(item)

sitemaps = {
    'posts': PostSitemap,
    'roots': RootSitemap
}