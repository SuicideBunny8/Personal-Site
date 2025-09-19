from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail


class ContactForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    subject = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)

    def send(self):
        subject = self.cleaned_data.get('subject')
        email   = self.cleaned_data.get('email')
        name    = self.cleaned_data.get('name')
        text    = self.cleaned_data.get('text')
        body_text = f"From: {name}, {email}\n\n{text}"
        try:
            send_mail(subject, body_text, None, recipient_list=["emelavm@gmail.com"], fail_silently=False)
            return True
        except:
            self.add_error(None, ValidationError("Could not send mail"))
            return False