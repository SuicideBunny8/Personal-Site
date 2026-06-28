"""
URL configuration for personalsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import urls as auth_urls
from django.contrib.auth.decorators import login_required
from django.contrib.flatpages import views as flatpage_views
from django.contrib.flatpages import urls as flatpage_urls
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import index as site_index_view
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.contrib import admin
from django.urls import include, path
from django.urls import include, path
from django.views.decorators.cache import never_cache

from .views import robots_txt
from .sitemaps import sitemaps as sitemaps_dict

import os


admin_url = os.environ['DJANGO_ADMIN_URL']

urlpatterns = [
    path('admin/'  , include('admin_honeypot.urls', namespace='admin_honeypot')), # honeypot URL
    path(admin_url + '/', admin.site.urls), # import from secrets so not exposed on git
    path('', include("blog.urls")),
    # ckeditor 5
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    # contact page
    path('contact/', include("contact.urls")),
    path('captcha/', include('captcha.urls')),
    # flatpages
    path('about/', flatpage_views.flatpage, kwargs={"url": "/about/"}, name='about'),
    path('sitemap.xml', sitemap_view, {'sitemaps': sitemaps_dict}),
    path("robots.txt", robots_txt),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()