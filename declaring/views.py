from .models import Entry, Goods
from user.models import Document
from .forms import EntryForm, GoodsFormSet
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
import datetime
from django.db import transaction
from django.http import HttpResponseRedirect


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

    # def get_context_data(self, **kwargs):
    #     data = super(EntryUpdateView, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         data['goods'] = GoodsFormSet(
    #             self.request.POST, instance=self.object)
    #     else:
    #         data['goods'] = GoodsFormSet(instance=self.object)
    #     return data

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     formset = context['goods']
    #     with transaction.atomic():
    #         form.instance.user_id = self.request.user.id
    #         self.object = form.save()
    #         if formset.is_valid():
    #             formset.instance = self.object
    #             formset.save()
    #     return super(EntryUpdateView, self).form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     context = self.get_context_data()
    #     formset = context['goods']
    #     with transaction.atomic():
    #         form.instance.user_id = self.request.user.id
    #         self.object = form.save()
    #         if formset.is_valid():
    #             formset.instance = self.object
    #             formset.save()
    #     # if form.is_valid():
    #     #     entry_edit = form.save(commit=False)
    #     #     entry_edit.save()
    #             return redirect('entry_list')
    #         else:
    #             return super(EntryUpdateView, self).get(request, *args, **kwargs)


class EntryDeleteView(SuccessMessageMixin, DeleteView):
    """Delete a selected entry"""
    model = Entry
    success_url = reverse_lazy('entry_list')
    success_message = _('Митну декларацію успішно видалено')

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
