from django.db import models
from django.urls import reverse

import re

# Create your models here.
# https://docs.djangoproject.com/en/5.2/ref/models/fields/

class Post(models.Model):
    title = models.CharField(
        max_length=100,
        help_text = "Title to be displayed on the psot itself"
        )
    
    slug = models.SlugField(
        max_length=100,
        help_text='A label for URL config'
        )
    
    text = models.TextField(
        blank=True,
        help_text = "Blog post content. Formatting should be in HTML"
        )
    
    pub_date = models.DateField(
        'date published',
        auto_now_add=True,
        )
    
    rank = models.PositiveIntegerField(
        default=0,
        #editable=False,
        help_text = "What order to list popular posts in. not yet implemented"
        )
    
    # Flags
    draft = models.BooleanField(
        default=True,
        help_text='Set True to keep the post from being listed on the site. Use for in progress posts'
        )
    
    featured = models.BooleanField(
        default=False,
        help_text='Set True if the post should be highlighted on the front page of the site'
        )
    
    # Key Media
    banner = models.ImageField(
        upload_to='post_banners',
        blank=True,
        help_text = "Image to be displayed on featured cards and at the top of post pages."
        )
    
    icon = models.ImageField(
        upload_to='post_icons',
        blank=True,
        help_text = "Image to be displayed in post list cards"
        )
    
    # meta fields
    meta_title = models.CharField(
        max_length=60,
        default="CHANGE ME",
        help_text = "Title to be displayed in tab label and search results. Helps SEO"
        )

    meta_description = models.CharField(
        max_length=150,
        default="CHANGE ME",
        help_text = "Description to be listed in the head meta description. Helps with SEO"
        )

    class Meta:
        verbose_name = 'blog post'
        ordering = ['-pub_date', 'title']
        get_latest_by = 'pub_date'
    
    def short_text(self):
        if len(self.text) > 20: # TODO: refine length
            short = ' '.join(self.text.split()[:20])
            short += ' ...'
        else:
            short = self.text

        # process to terminate any unclosed tags
        tag_stack = []

        for tag in re.finditer(r"(<\w+>)|(<\/\w+>)", short):
            tagstr = tag.group()
            if tagstr[1] == "/":
                #terminator
                match = tagstr.replace("/", "")
                
                temp_stack = []
                while not tag_stack[-1] == match:
                    temp_stack.append(tag_stack.pop())
                
                if len(tag_stack) > 0:
                    tag_stack.pop()
                
                while len(temp_stack) > 0:
                    tag_stack.append(temp_stack.pop())
                
                pass
            else:
                #opener
                tag_stack.append(tagstr)

        for unclosed in tag_stack[::-1]:
            short += (unclosed[:1] + "/" + unclosed[1:])
        return short
    
    def get_absolute_url(self):
        return reverse('post_view', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title