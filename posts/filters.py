import django_filters
from django import forms
from django.utils.safestring import mark_safe


class DateWidget(forms.DateInput):
    """Widget for date input"""
    input_type = 'date'


class OrderWidget(django_filters.widgets.LinkWidget):
    """Widget for ordering of object list"""

    def render(self, name, value, attrs=None, choices=(), renderer=None):
        if not hasattr(self, 'data'):
            self.data = {}
        if value is None:
            value = ''
        output = []
        options = self.render_options(choices, [value], name)
        if options:
            output.append(options)
        return mark_safe('\n'.join(output))

    def option_string(self):
        return '<a class="dropdown-item p-0 %(attrs)s" href="?%(query_string)s">%(label)s</a>'


class TopicFilter(django_filters.FilterSet):
    """Functionality of topics filter button"""
    order = django_filters.OrderingFilter(
        fields=(
            ('author', 'автору'),
            ('title', 'заголовку'),
            ('created', 'даті публікації'),
        ),
        widget=OrderWidget
    )
    author = django_filters.CharFilter(
        field_name='author',
        lookup_expr='icontains'
    )
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains'
    )
    description = django_filters.CharFilter(
        field_name='description',
        lookup_expr='icontains'
    )
    created__gte = django_filters.DateFilter(
        field_name='created',
        label='Опубліковано з',
        lookup_expr='gte',
        widget=DateWidget
    )
    created__lte = django_filters.DateFilter(
        field_name='created',
        label='по',
        lookup_expr='lte',
        widget=DateWidget
    )
    updated__gte = django_filters.DateFilter(
        field_name='updated',
        label='Редаговано з',
        lookup_expr='gte',
        widget=DateWidget
    )
    updated__lte = django_filters.DateFilter(
        field_name='updated',
        label='по',
        lookup_expr='lte',
        widget=DateWidget
    )


class PostFilter(django_filters.FilterSet):
    """Functionality of posts filter button"""
    order = django_filters.OrderingFilter(
        fields=(
            ('author', 'автору'),
            ('title', 'заголовку'),
            ('created', 'опублікуванню'),
            ('updated', 'редагуванню'),
        ),
        widget=OrderWidget
    )
    author = django_filters.CharFilter(
        field_name='author',
        lookup_expr='icontains'
    )
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains'
    )
    preview = django_filters.CharFilter(
        field_name='preview',
        lookup_expr='icontains'
    )
    content = django_filters.CharFilter(
        field_name='content',
        lookup_expr='icontains'
    )
    created__gte = django_filters.DateFilter(
        field_name='created',
        label='Опубліковано з',
        lookup_expr='gte',
        widget=DateWidget
    )
    created__lte = django_filters.DateFilter(
        field_name='created',
        label='по',
        lookup_expr='lte',
        widget=DateWidget
    )
    updated__gte = django_filters.DateFilter(
        field_name='updated',
        label='Редаговано з',
        lookup_expr='gte',
        widget=DateWidget
    )
    updated__lte = django_filters.DateFilter(
        field_name='updated',
        label='по',
        lookup_expr='lte',
        widget=DateWidget
    )
