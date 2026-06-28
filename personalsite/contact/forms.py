from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from smtplib import SMTPException

from captcha.fields import CaptchaField

from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={"placeholder": "John.Doe@example.com"}))
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "John Doe", "class": "requried"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "requried"}))
    captcha = CaptchaField()

    class Meta:
        model = ContactSubmission
        fields = ["email", "name", "message"]
        help_texts = {
            "email": "Your Email (optional)",
            "name": "Your Name",
            "message": "Your Message"
        }
        labels = {
            "email": "Email",
            "name": "Name",
            "message": "Message"
        }