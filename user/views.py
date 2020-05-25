from .models import User, Document, Vehicle
from declaring.models import Entry
from posts.models import Post
from .forms import UserForm, DocumentForm, VehicleForm
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect


class ProfileView(UpdateView):
    """Updating of user data"""
    model = User
    form_class = UserForm
    template_name = 'user/profile_personal.html'
    success_url = '/user/profile/'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Total number of entries
        user_entries = Entry.objects.filter(user=self.request.user).count()
        context['user_entries'] = user_entries
        # Total number of posts
        user_posts = Post.objects.filter(author=self.request.user)
        context['user_posts'] = user_posts.count()
        # Total number of comments
        total_comments = 0
        for post in user_posts:
            total_comments += int(post.comments.count())
        context['user_comments'] = total_comments
        # Total number of likes
        total_likes = 0
        for post in user_posts:
            total_likes += int(post.likes.count())
        context['user_likes'] = total_likes
        context['user'] = self.request.user
        return context


class DocumentListView(ListView):
    """Display list of user's existing documents"""
    model = Document
    template_name = 'user/profile_documents.html'
    success_url = reverse_lazy('profile_documents')
    paginate_by = 5

    def get_queryset(self):
        return Document.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Total number of entries
        user_entries = Entry.objects.filter(user=self.request.user).count()
        context['user_entries'] = user_entries
        # Total number of posts
        user_posts = Post.objects.filter(author=self.request.user)
        context['user_posts'] = user_posts.count()
        # Total number of comments
        total_comments = 0
        for post in user_posts:
            total_comments += int(post.comments.count())
        context['user_comments'] = total_comments
        # Total number of likes
        total_likes = 0
        for post in user_posts:
            total_likes += int(post.likes.count())
        context['user_likes'] = total_likes
        context['user'] = self.request.user
        return context


class DocumentCreateView(SuccessMessageMixin, CreateView):
    """Creating of a document"""
    model = Document
    form_class = DocumentForm
    template_name = 'user/profile_document_create.html'
    success_url = reverse_lazy('profile_documents')
    success_message = _(
        'Інформацію про документ успішно створено та збережено')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(DocumentCreateView, self).form_valid(form)


class DocumentUpdateView(SuccessMessageMixin, UpdateView):
    """Updating of an existing document"""
    model = Document
    form_class = DocumentForm
    template_name = 'user/profile_document_update.html'
    success_url = reverse_lazy('profile_documents')
    success_message = _('Інформацію про документ успішно оновлено')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            doc_edit = form.save(commit=False)
            doc_edit.save()
            return redirect('profile_documents')
        else:
            return super(DocumentUpdateView, self).get(request, *args, **kwargs)


class DocumentDeleteView(SuccessMessageMixin, DeleteView):
    """Delete selected document"""
    model = Document
    success_url = reverse_lazy('profile_documents')
    success_message = _('Інформацію про документ успішно видалено')

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


class VehicleListView(ListView):
    """Display list of user's existing vehicles"""
    model = Vehicle
    template_name = 'user/profile_vehicles.html'
    success_url = reverse_lazy('profile_vehicles')
    paginate_by = 5

    def get_queryset(self):
        return Vehicle.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Total number of entries
        user_entries = Entry.objects.filter(user=self.request.user).count()
        context['user_entries'] = user_entries
        # Total number of posts
        user_posts = Post.objects.filter(author=self.request.user)
        context['user_posts'] = user_posts.count()
        # Total number of comments
        total_comments = 0
        for post in user_posts:
            total_comments += int(post.comments.count())
        context['user_comments'] = total_comments
        # Total number of likes
        total_likes = 0
        for post in user_posts:
            total_likes += int(post.likes.count())
        context['user_likes'] = total_likes
        context['user'] = self.request.user
        return context


class VehicleCreateView(SuccessMessageMixin, CreateView):
    """Creating of a vehicle"""
    model = Vehicle
    form_class = VehicleForm
    template_name = 'user/profile_vehicle_create.html'
    success_url = reverse_lazy('profile_vehicles')
    success_message = _(
        'Інформацію про транспортний засіб успішно створено та збережено')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(VehicleCreateView, self).form_valid(form)


class VehicleUpdateView(SuccessMessageMixin, UpdateView):
    """Updating of an existing vehicle"""
    model = Vehicle
    form_class = VehicleForm
    template_name = 'user/profile_vehicle_update.html'
    success_url = reverse_lazy('profile_vehicles')
    success_message = _('Інформацію про транспортний засіб успішно оновлено')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            auto_edit = form.save(commit=False)
            auto_edit.save()
            return redirect('profile_vehicles')
        else:
            return super(VehicleUpdateView, self).get(request, *args, **kwargs)


class VehicleDeleteView(SuccessMessageMixin, DeleteView):
    """Delete selected vehicle"""
    model = Vehicle
    success_url = reverse_lazy('profile_vehicles')
    success_message = _('Інформацію про транспортний засіб успішно видалено')

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
