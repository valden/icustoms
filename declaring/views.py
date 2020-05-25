from .models import Entry, Goods
from user.models import Document
from .forms import EntryForm, GoodsFormSet
from django.views.generic import View, DetailView, CreateView, UpdateView, ListView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect, render
import datetime
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from core import settings
from django.template.loader import render_to_string
import os
from django.core.mail import EmailMessage
from django.contrib import messages


class EntryListView(ListView):
    """Display list of user's existing entries"""
    model = Entry
    template_name = 'declaring/entry_list.html'
    success_url = reverse_lazy('entry_list')
    paginate_by = 5

    def get_queryset(self):
        return Entry.objects.filter(user_id=self.request.user.id).order_by('-update_date')


class EntryCreateView(SuccessMessageMixin, CreateView):
    """Creating of a new entry"""
    model = Entry
    form_class = EntryForm
    template_name = 'declaring/entry_create.html'
    success_url = reverse_lazy('entry_list')
    success_message = _('Митну декларацію успішно збережено')

    def get_form_kwargs(self):
        kwargs = super(EntryCreateView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def get_context_data(self, **kwargs):
        data = super(EntryCreateView, self).get_context_data(**kwargs)
        data['goods'] = GoodsFormSet(
            self.request.POST or None, self.request.FILES or None)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['goods']
        with transaction.atomic():
            form.instance.user_id = self.request.user.id
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super(EntryCreateView, self).form_valid(form)


class EntryUpdateView(SuccessMessageMixin, UpdateView):
    """Updating of an existing entry"""
    model = Entry
    form_class = EntryForm
    template_name = 'declaring/entry_update.html'
    success_url = reverse_lazy('entry_list')
    success_message = _('Відомості митної декларації успішно оновлено')

    def get_form_kwargs(self):
        kwargs = super(EntryUpdateView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        goods_form = GoodsFormSet(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, goods_form=goods_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        goods_form = GoodsFormSet(self.request.POST, instance=self.object)

        if (form.is_valid() and goods_form.is_valid()):
            return self.form_valid(form, goods_form)
        return self.form_invalid(form, goods_form)

    def form_valid(self, form, goods_form):
        self.object = form.save()
        goods_form.instance = self.object
        goods_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, goods_form):
        return self.render_to_response(self.get_context_data(form=form, goods_form=goods_form))


class EntryDeleteView(SuccessMessageMixin, DeleteView):
    """Delete a selected entry"""
    model = Entry
    success_url = reverse_lazy('entry_list')
    success_message = _('Митну декларацію успішно видалено')

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


# class EntryPdfView(DetailView):
#     """Display a selected entry in pdf format"""
#     model = Entry
#     template_name = 'declaring/entry_form.html'

#     def get_success_url(self):
#         return reverse('entry_pdf', kwargs={'pk': self.object.pk})

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         Entry.objects.filter(pk=self.object.pk)
#         context = self.get_context_data(object=self.object)
#         return self.render_to_response(context)

    # def get_context_data(self, **kwargs):
    #     context = super(EntryPdfView, self).get_context_data(**kwargs)
    #     context['entry'] = Entry.objects.filter(id=self.object.pk)
    #     return context


class EntryPreView(DetailView):
    model = Entry
    template_name = 'declaring/entry_preview.html'


class EntryPrintView(DetailView):
    model = Entry
    template_name = 'declaring/entry_print.html'


class EntrySendEmail(DetailView):
    model = Entry
    template_name = 'declaring/entry_print.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        content = render_to_string('declaring/entry_print.html', context)
        with open('entry.html', 'w', encoding='UTF-8') as static_file:
            static_file.write(content)
        msg = EmailMessage(
            _('Ваша митна декларація'),
            _('У додатку до цього листа надіслано підготовлену Вами митну декларацію'),
            'info@icustoms.info',
            [request.user.email],
        )
        msg.content_subtype = "html"
        msg.attach_file('entry.html')
        msg.send()
        os.remove('entry.html')
        messages.success(request, _(
            'Митну декларацію успішно відправлено на Вашу поштову скриньку %s') % request.user.email)
        return redirect('entry_list')
