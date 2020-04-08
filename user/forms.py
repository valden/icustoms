from django import forms
from django.conf import settings
from .models import User, Document, Vehicle
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout,
                                 Fieldset,
                                 Field,
                                 Div,
                                 MultiField,
                                 ButtonHolder,
                                 Submit,
                                 Button,
                                 HTML)
from crispy_forms.bootstrap import AppendedText, FormActions
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


class UserForm(forms.ModelForm):
    birthday = forms.DateField(
        label=_('День народження'),
        input_formats=settings.DATE_INPUT_FORMATS,
        required=False)
    terms = forms.BooleanField(
        label=_('Я ознайомився(лась) і погоджуюсь з правилами та умовами'),
        initial=False,
        required=True,
        error_messages={
            'required': _('Ви повинні ознайомитись та погодитись з умовами')
        }
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'residence',
            'nationality',
            'birthday',
            'image',
            'terms',
        )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset(
                "Інфрмація для заповнення митної декларації",
                'first_name',
                'middle_name',
                'last_name',
                'email',
                'residence',
                'nationality',
                Field(
                    AppendedText(
                        'birthday',
                        mark_safe('<span class="fa fa-calendar-alt"></span>'),
                        placeholder=_("dd/mm/yyyy"), css_class='form-control datepicker', active=True
                    )
                ),
                'image',
                'terms',
                FormActions(ButtonHolder(
                    Submit('submit', _('Зберегти'), css_class='btn btn-sm btn-secondary'))),
            )
        )


class DocumentForm(forms.ModelForm):
    doc_date = forms.DateField(
        label=_('Дата видачі'),
        input_formats=settings.DATE_INPUT_FORMATS,
        required=True
    )

    class Meta:
        model = Document
        fields = (
            'doc_name',
            'doc_number',
            'doc_date',
        )

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'doc_name',
                'doc_number',
                Field(
                    AppendedText(
                        'doc_date',
                        mark_safe('<span class="fa fa-calendar-alt"></span>'),
                        placeholder=_("dd/mm/yyyy"), css_class='form-control datepicker', active=True
                    )
                ),
                FormActions(ButtonHolder(
                    Submit('submit', _('Зберегти'),
                           css_class='btn btn-sm btn-secondary'),
                    HTML('<a class="btn btn-sm btn-default" href={% url "profile_documents" %}>Відмінити</a>')))
            )
        )


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            'auto_name',
            'auto_year',
            'auto_engine',
            'auto_vin'
        )

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset(
                "",
                'auto_name',
                'auto_year',
                'auto_engine',
                'auto_vin',
                # Field(
                #     AppendedText(
                #         'doc_date',
                #         mark_safe('<span class="fa fa-calendar-alt"></span>'),
                #         placeholder=_("dd/mm/yyyy"), css_class='form-control datepicker', active=True
                #     )
                # ),
                FormActions(ButtonHolder(
                    Submit('submit', _('Зберегти'),
                           css_class='btn btn-sm btn-secondary'),
                    HTML('<a class="btn btn-sm btn-default" href={% url "profile_vehicles" %}>Відмінити</a>')))
            )
        )
