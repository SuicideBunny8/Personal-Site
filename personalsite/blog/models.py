from django.db import models
from django.utils import timezone
from django.urls import reverse

from .utils import strip_tags

import re

# Create your models here.
# https://docs.djangoproject.com/en/5.2/ref/models/fields/

class PostStatus(models.TextChoices):
    DRAFT     = 'draft',    'Draft'
    PUBLISHED = 'published','Published'
    FEATURED  = 'featured', 'Featured'
    ARCHIVED  = 'archived', 'Archived'

class Tag(models.Model):
    name = models.CharField(
        max_length=32,
        unique=True)

    slug = models.SlugField(
        max_length=32,
        unique=True,
        help_text='A label for URL config.')

    def get_absolute_url(self):
        # TODO: tags needs fleshing out
        #return reverse('tag_detail', kwargs={'slug': self.slug})
        # placeholder while tags pages are not user exposed to prevent potential accidental crashes
        return reverse('homepage')

    def __str__(self):
        return self.name

class Post(models.Model):
    def banner_upload_path(instance, filename):
        return f"post_banners/{instance.slug}/{filename}"

    def icon_upload_path(instance, filename):
        return f"post_icons/{instance.slug}/{filename}"
    
    title = models.CharField(
        max_length=100,
        help_text = "Title to be displayed on the post itself"
        )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text='A label for URL config'
        )
    
    text = models.TextField(
        blank=True,
        help_text = "Blog post content. Formatting should be in HTML"
        )
    
    pub_date = models.DateField(
        'date published',
        default=timezone.localdate,
        blank=True,
        db_index=True
        )

    rank = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text = "What order to list popular posts in. not yet implemented"
        )
    
    # Flags
    status = models.CharField(
        max_length=16,
        choices=PostStatus.choices,
        default=PostStatus.DRAFT,
        db_index=True
    )
    
    # Key Media
    banner = models.ImageField(
        upload_to=banner_upload_path,
        blank=True,
        help_text = "Image to be displayed on featured cards and at the top of post pages."
        )
    
    icon = models.ImageField(
        upload_to=icon_upload_path,
        blank=False,
        help_text = "Image to be displayed in post list cards"
        )
    
    # html meta fields
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text = "Title to be displayed in tab label and search results. Helps SEO"
        )

    meta_description = models.CharField(
        max_length=150,
        blank=True,
        help_text = "Description to be listed in the head meta description. Helps with SEO"
        )

    tags = models.ManyToManyField(
        Tag,
        blank=True
    )

    # automatically assigned at save
    updated_at = models.DateTimeField(
        auto_now=True
        )
    
    short_text = models.TextField(
        blank=True,
        editable=False
        )

    class Meta:
        verbose_name = 'blog post'
        ordering = ['-pub_date', 'title']
        get_latest_by = 'pub_date'
        indexes = [
            models.Index(
                fields=['-pub_date', 'status'],
                name='post_pubdate_status_idx'
            ),
        ]
    
    def get_absolute_url(self):
        return reverse('post_view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        short_text_length = 40

        text_splt = strip_tags(self.text).split()
        if text_splt.length > short_text_length:
            self.short_text = ' '.join(text_splt[:short_text_length]) + '...'
        else:
            self.short_text = ' '.join(text_splt)

        # default meta title
        if not self.meta_title:
            self.meta_title = self.title[:60]

        # default meta description
        if not self.meta_description:
            self.meta_description = self.short_text

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Post id={self.pk} slug={self.slug} status={self.status}>"