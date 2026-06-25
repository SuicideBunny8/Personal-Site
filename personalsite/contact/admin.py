from django.contrib import admin

from .models import ContactSubmission

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_date')
    list_filter = ('name', 'sub_date')
    search_fields = ('name',)

admin.site.register(ContactSubmission, ContactAdmin)