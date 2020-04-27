from django import forms
from django.forms.formsets import TOTAL_FORM_COUNT
from django.conf import settings
from .models import Entry, Goods
from user.models import Document, Vehicle
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, ButtonHolder, Div, Field, Fieldset, HTML, Layout, MultiField, Row, Submit
from crispy_forms.bootstrap import Accordion, AccordionGroup, AppendedText, FormActions, InlineRadios
from django.forms.models import BaseInlineFormSet, formset_factory, inlineformset_factory, modelformset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from datetime import datetime


class DocumentModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return "%s від %s №%s" % (object.doc_name, datetime.strftime(object.doc_date, settings.DATE_FORMAT), object.doc_number)


class VehicleModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return "%s %sр.в." % (object.auto_name, object.auto_year)


class EntryForm(forms.ModelForm):

    passport = DocumentModelChoiceField(
        label=_('Документ, що посвідчує особу'),
        queryset=Document.objects.none(),
        empty_label=_('Оберіть документ...'),
        widget=forms.Select(),
        required=False
    )
    vehicle = VehicleModelChoiceField(
        label=_('Транспортний засіб'),
        queryset=Vehicle.objects.none(),
        empty_label=_('Оберіть транспортний засіб...'),
        widget=forms.Select(),
        required=False
    )

    class Meta:
        model = Entry
        fields = (

            'direction',
            'passport',
            'departure',
            'arrival',
            'kids_number',
            'accamp_number',
            'nonaccamp_number',
            'cargo_number',
            'vehicle',
            'purpose',
            'limited',
        )
        widgets = {
            'direction': forms.RadioSelect(),
            'purpose': forms.RadioSelect(),
            'limited': forms.RadioSelect(),
        }

    def __init__(self, user_id, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)

        self.fields['passport'].queryset = Document.objects.filter(
            user_id=user_id)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(
            user_id=user_id)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.fields['kids_number'].label = False
        self.fields['accamp_number'].label = False
        self.fields['nonaccamp_number'].label = False
        self.fields['cargo_number'].label = False
        self.fields['limited'].label = False
        self.helper.layout = Layout(
            Fieldset(
                "",
                InlineRadios('direction')
            ),
            Fieldset(
                _('1. Відомості про особу'),
                'passport',
                'departure',
                'arrival'
            ),
            Fieldset(
                "Зі мною прямують неповнолітні діти",
                Field(
                    'kids_number',
                    placeholder=_('Кількість дітей')
                ),
                css_class='col-md-4'
            ),
            HTML('<hr>'),
            Fieldset(
                _('2. Відомості про спосіб переміщення товарів'),
                Row(
                    Div(
                        Fieldset(
                            _("2.1. Супроводжуваний багаж, ручна поклажа"),
                            Field(
                                'accamp_number',
                                placeholder=_('Кількість місць')
                            ),
                        ),
                        css_class='col-md-4'
                    ),
                    Div(
                        Fieldset(
                            _("2.2. Несупроводжуваний багаж"),
                            Field(
                                'nonaccamp_number',
                                placeholder=_('Кількість місць')
                            ),
                        ),
                        css_class='col-md-4'
                    ),
                    Div(
                        Fieldset(
                            _("2.3. Вантажне відправлення"),
                            Field(
                                'cargo_number',
                                placeholder=_('Кількість місць')
                            ),
                        ),
                        css_class='col-md-4'
                    ),
                ),
            ),
            HTML('<hr>'),
            Fieldset(
                _('3. Відомості про наявність товарів'),
                Fieldset(
                    _("3.2. Транспортний засіб особистого користування"),
                    'vehicle',
                    InlineRadios('purpose'),
                ),
                Fieldset(
                    _('''3.3. Товари, переміщення яких через державний кордон України
                    обмежено (здійснюється за дозвільними документами, що видаються
                    органами виконавчої влади) або заборонено'''),
                    InlineRadios('limited'),
                ),
            ),
            HTML('<hr>'),
            Fieldset(
                _('''4. Відомості про товари, що підлягають обов’язковому письмовому
                  декларуванню та/або оподаткуванню митними платежами, товари,
                  переміщення яких через державний кордон України заборонено
                  або здійснюється за дозвільними документами, що видаються
                  органами виконавчої влади, та інші товари, що декларуються
                  письмово за бажанням громадянина або на вимогу митного органу'''),
            ),
            HTML('<hr>'),
        )


class GoodsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GoodsForm, self).__init__(*args, **kwargs)

        # self.fields['passport'].queryset = Document.objects.filter(
        #     user_id=user_id)
        # self.fields['vehicle'].queryset = Vehicle.objects.filter(
        #     user_id=user_id)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.disable_csrf = True
        # self.helper.template = 'bootstrap4/table_inline_formset.html'

        self.helper.form_show_labels = False
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-lg-3'
        # self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(

            Fieldset(
                "",
                Row(
                    Div(
                        Field(
                            'goods_name',
                            placeholder=_(
                                'Найменування товару')
                        ),
                        css_class='col-md-5',

                    ),
                    Div(
                        Field(
                            'goods_number',
                            placeholder=_('Кількість')
                        ),
                        css_class='col-md-2'
                    ),
                    Div(
                        Field(
                            'goods_unit',

                        ),
                        css_class='col-md-1'
                    ),
                    Div(
                        Field(
                            'goods_value',
                            placeholder=_('Сума')
                        ),
                        css_class='col-md-2'
                    ),
                    Div(
                        Field(
                            'goods_currency',

                        ),
                        css_class='col-md-1'
                    ),
                    Div(
                        HTML(
                            '<i class="nav-icon fas fa-times-circle float-left mt-1" style="color:red"></i>'),
                        Field(
                            'DELETE',
                        ),
                        css_class='col-md-1 tools'
                    ),
                ),
                css_class='formset'
            ),

        )

    class Meta:
        model = Goods
        exclude = ()


# class AddableFormSet(BaseInlineFormSet):
#     can_add_form = True

#     def add_form(self, **kwargs):
#         self.forms.append(self._construct_form(
#             self.total_form_count(), **kwargs))
#         self.forms[-1].is_bound = False
#         self.data = self.data.copy()
#         self.data['%s-%s' % (self.management_form.prefix, TOTAL_FORM_COUNT)
#                   ] = self.management_form.cleaned_data[TOTAL_FORM_COUNT] + 1

#     @property
#     def add_form_key(self):
#         return self.add_prefix(ADD_FORM_KEY)


GoodsFormSet = inlineformset_factory(
    Entry, Goods,
    form=GoodsForm,
    # formset=AddableFormSet,
    fields=(
        'goods_name',
        'goods_number',
        'goods_unit',
        'goods_value',
        'goods_currency',

    ),
    extra=1,
    can_delete=True
)
