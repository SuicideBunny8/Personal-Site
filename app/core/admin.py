from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage

from django_ckeditor_5.widgets import CKEditor5Widget

FLATPAGE_TEMPLATES = (("flatpage.html","flatpage"),)

# overriding flatpage editor
class FlatPageCustomForm(FlatpageForm):
    template_name = forms.ChoiceField(choices=FLATPAGE_TEMPLATES)

    class Meta(FlatpageForm.Meta):
    	widgets = {'content': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="default"
              	)}

class FlatPageCustomAdmin(FlatPageAdmin):
	form = FlatPageCustomForm
	# formfield_overrides = {
    #     models.TextField: {'widget': CKEditor5Widget}
    # }

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustomAdmin)