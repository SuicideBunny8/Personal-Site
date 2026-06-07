from django import forms
from django.contrib import admin
from .models import Post, Tag
from django_ckeditor_5.widgets import CKEditor5Widget

# Register your models here.

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
              "text": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="default"
              )
          }

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    list_filter = ('title', 'pub_date')
    search_fields = ('title',)
    prepopulated_fields  = {"slug": ("title",)}
    filter_horizontal = ('tags',)
    form = PostAdminForm

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)