from django import forms
from django.contrib import admin
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Register your models here.

class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    list_filter = ('title', 'pub_date')
    search_fields = ('title',)
    prepopulated_fields  = {"slug": ("title",)}
    form = PostAdminForm

admin.site.register(Post, PostAdmin)