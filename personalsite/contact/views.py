from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib import messages
from .forms import ContactForm

# Create your views here.
class ContactView(View):
    form_class = ContactForm
    template_name = 'contact/contact_form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            mail_sent = bound_form.send()
            if mail_sent:
                messages.success(request, "Thank you for your comments!")
                return redirect('homepage')
        return render(request, self.template_name, {'form': bound_form})