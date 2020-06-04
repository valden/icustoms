from django import forms
from django.forms.formsets import TOTAL_FORM_COUNT
from django.conf import settings
from .models import Entry, Goods
from user.models import Document, Vehicle
from deskbooks.models import BorderPoint
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, ButtonHolder, Div, Field, Fieldset, HTML, Layout, MultiField, Row, Submit
from crispy_forms.bootstrap import Accordion, AccordionGroup, AppendedText, FormActions, InlineRadios
from django.forms.models import BaseInlineFormSet, formset_factory, inlineformset_factory, modelformset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from datetime import datetime


class BorderModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return "%s | %s" % (object.region, object.ukr)


class DocumentModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return "%s від %s №%s" % (object.doc_name, datetime.strftime(object.doc_date, settings.DATE_FORMAT), object.doc_number)


class VehicleModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, object):
        return "%s %sр.в." % (object.auto_name, object.auto_year)


class EntryForm(forms.ModelForm):

    border_point = BorderModelChoiceField(
        label=_('Пункт пропуску'),
        queryset=BorderPoint.objects.all(),
        empty_label=_('Оберіть пункт пропуску...'),
        widget=forms.Select(),
        required=False
    )
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
            'border_point',
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
                "",
                Field(
                    'border_point',
                    title=_(
                        '''Заповнюється для інформування про ситуацію в пункті пропуску, через який планується перетин кордону'''
                    )
                )
            ),
            Fieldset(
                _('1. Відомості про особу'),
                Field(
                    'passport',
                    title=_(
                        '''Обирається з переліку, який створено користувачем у власному профілі'''
                    )
                ),
                Field(
                    'departure',
                    title=_(
                        '''Країна, з якої прибув (згідно з документами, що підтверджують маршрут прямування, у разі їх наявності)'''
                    )
                ),
                Field(
                    'arrival',
                    title=_(
                        '''Країна, до якої прямує (згідно з документами, що підтверджують маршрут прямування, у разі їх наявності)'''
                    )
                ),
            ),
            Fieldset(
                "Зі мною прямують неповнолітні діти",
                Field(
                    'kids_number',
                    placeholder=_('Кількість дітей'),
                    title=_(
                        '''Наявність (відсутність) дітей віком до 16 років, які супроводжуються громадянином і перетинають митний кордон України разом з ним, із зазначенням кількості (цифрами та словами) таких дітей'''
                    )
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
                                placeholder=_('Кількість місць'),
                                title=_(
                                    '''Зазначаються дані про наявність (відсутність) супроводжуваного багажу та ручної поклажі, а також про кількість їх місць'''
                                )
                            ),
                        ),
                        css_class='col-md-4'
                    ),
                    Div(
                        Fieldset(
                            _("2.2. Несупроводжуваний багаж"),
                            Field(
                                'nonaccamp_number',
                                placeholder=_('Кількість місць'),
                                title=_(
                                    '''Зазначаються дані про наявність (відсутність) несупроводжуваного багажу і про кількість його місць'''
                                )
                            ),
                        ),
                        css_class='col-md-4'
                    ),
                    Div(
                        Fieldset(
                            _("2.3. Вантажне відправлення"),
                            Field(
                                'cargo_number',
                                placeholder=_('Кількість місць'),
                                title=_(
                                    '''Заповнюється у разі відправлення громадянином товарів за межі митної території України у вантажному відправленні'''
                                )
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
                    Field(
                        'vehicle',
                        title=_(
                            '''Обирається з переліку, який створено користувачем у власному профілі'''
                        )
                    ),
                    InlineRadios('purpose'),
                    title=_(
                        '''Наводяться детальні відомості про транспортний засіб особистого користування, що тимчасово ввозиться на митну територію України, ввозиться на митну територію України з метою транзиту або зворотно вивозиться за межі митної території України. У полі для зазначення мети переміщення транспортного засобу особистого користування через митний кордон України ставиться позначка в потрібній рамці'''
                    )
                ),
                Fieldset(
                    _('''3.3. Товари, переміщення яких через державний кордон України
                    обмежено (здійснюється за дозвільними документами, що видаються
                    органами виконавчої влади) або заборонено'''),
                    InlineRadios(
                        'limited',
                        title=_(
                            '''Заповнення здійснюється шляхом проставлення позначки у відповідній рамці: „Так” - за наявності товарів переміщення, „Ні” - за їх відсутності'''
                        )
                    ),
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
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.disable_csrf = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row(
                    Div(
                        Field(
                            'goods_name',
                            placeholder=_('Найменування товару'),
                            title=_('''Зазначаються точні дані про товари (назви, характеристики товарів, відмітні ознаки тощо), необхідні для їх ідентифікації, а також реквізити:
- дозвільних документів (найменування, номер і дата видачі дозвільного документа й орган, що його видав) - у разі декларування товарів з поданням дозвільних документів, які є підставою для пропуску товарів через митний кордон України;
- документів, що є документальним підтвердженням для надання пільг в оподаткуванні (вид, номер і дата документа), - при здійсненні митного оформлення товарів з наданням пільг в оподаткуванні.''')
                        ),
                        css_class='col-md-5',

                    ),
                    Div(
                        Field(
                            'goods_number',
                            placeholder=_('Кількість'),
                            title=_(
                                '''Зазначається вага або кількість задекларованих товарів за кожним найменуванням (цифрами та словами)''')
                        ),
                        css_class='col-md-2'
                    ),
                    Div(
                        Field(
                            'goods_unit',
                            title=_(
                                '''Обирається одиниця виміру ваги/кількості''')
                        ),
                        css_class='col-md-1'
                    ),
                    Div(
                        Field(
                            'goods_value',
                            placeholder=_('Сума'),
                            title=_(
                                '''Зазначається фактурна вартість задекларованих товарів''')
                        ),
                        css_class='col-md-2'
                    ),
                    Div(
                        Field(
                            'goods_currency',
                            title=_(
                                '''Обирається валюта фактурної вартості задекларованих товарів''')
                        ),
                        css_class='col-md-1'
                    ),
                    Div(
                        HTML(
                            '<i class="nav-icon fas fa-times-circle float-left mt-1" style="color:red"></i>'),
                        Field(
                            'DELETE',
                            title=_(
                                'В разі проставлення позначки після зберігання МД товар буде видалено із переліку')
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


GoodsFormSet = inlineformset_factory(
    Entry, Goods,
    form=GoodsForm,
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
