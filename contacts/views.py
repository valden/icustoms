from django import http
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import ContactForm
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from core import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.safestring import SafeString


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = "contacts/contacts.html"
    success_url = reverse_lazy('contacts')

    def get_form_kwargs(self):
        user = self.request.user
        form_kwargs = super(ContactFormView, self).get_form_kwargs()
        if user.is_authenticated:
            form_kwargs.update({
                'initial': {
                    'name': user.get_full_name,
                    'email': user.email
                }
            })
        return form_kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if request.user.is_authenticated:
                contact_name = request.user.get_full_name()
                contact_email = request.user.email
            else:
                contact_name = form.cleaned_data.get('name')
                contact_email = form.cleaned_data.get('email')
            contact_message = "{name}: ".format(
                name=contact_name)
            contact_message += "<br>{0}".format(
                SafeString(form.cleaned_data.get('message')))
            subject = form.cleaned_data.get('subject')
            msg = EmailMessage(
                subject,
                SafeString(contact_message),
                contact_email,
                ['contacts@icustoms.info'],
            )
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, _('Повідомлення успішно відправлено'))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
