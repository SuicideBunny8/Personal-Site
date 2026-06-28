from django.contrib import admin

from .models import ContactSubmission

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_date', 'read')
    list_filter = ('name', 'sub_date', 'read')
    search_fields = ('name',)
    read_only_fields = ('name', 'email', 'sub_date', 'message')

    def change_view(self, request, object_id, *args, **kwargs):
        ContactSubmission.objects.filter(pk=object_id).update(read=True)
        return super().change_view(request, object_id, *args, **kwargs)

admin.site.register(ContactSubmission, ContactAdmin)