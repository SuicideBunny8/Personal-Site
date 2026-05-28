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
from django.contrib.sitemaps.views import index as site_index_view
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.contrib import admin
from django.urls import include, path
from django.urls import include, path
from django.views.decorators.cache import never_cache

from ckeditor_uploader import views as ckeditor_views

from .sitemaps import sitemaps as sitemaps_dict

urlpatterns = [
    path('', include("blog.urls")),
    path('admin/'  , include('admin_honeypot.urls', namespace='admin_honeypot')), # honeypot URL
    path('elephant-pants/', admin.site.urls),
    path('contact/', include("contact.urls")),
    path('ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
    # flatpages
    path('about/', flatpage_views.flatpage, kwargs={"url": "/about/"}, name='about'),
    path('sitemap.xml', sitemap_view, {'sitemaps': sitemaps_dict}),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()