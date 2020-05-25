from django import forms, http
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.template import loader
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import ButtonHolder, Field, Fieldset, Layout, Submit


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label=_("Ім'я"))
    email = forms.EmailField(max_length=200, label=_("Email"))
    subject = forms.CharField(max_length=200, label=_("Тема"))
    message = forms.CharField(widget=forms.Textarea, label=_("Повідомлення"))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset(
                "",
                Field('name', id="name"),
                Field('email', id="email"),
                Field('subject', id="subject"),
                Field('message', id="message"),
                FormActions(ButtonHolder(
                    Submit('submit', _('Надіслати'), css_class='btn btn-sm btn-success')),
                    css_class="float-right"
                ),
            )
        )
