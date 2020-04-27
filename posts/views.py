from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.db.models import F
from django.views.generic import (
    TemplateView,
    DetailView,
    RedirectView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Topic, Post, Comment
from .forms import TopicForm, PostForm, CommentForm
from .filters import TopicFilter, PostFilter
from django.utils.translation import ugettext_lazy as _


class TopicListView(FilterView):
    """Listing of topics in a forum"""
    model = Topic
    template_name = 'posts/topic-list.html'
    paginate_by = 10
    filterset_class = TopicFilter

    def get_queryset(self):
        return Topic.objects.all()

    def get_success_url(self):
        return reverse('post_list', kwargs={'topic': self.object.pk})


class TopicCreateView(SuccessMessageMixin, CreateView):
    """Creating of a new topic in a forum"""
    model = Topic
    form_class = TopicForm
    template_name = 'posts/topic-new.html'
    success_url = reverse_lazy('topic_list')
    success_message = _('Тему успішно створено')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            post_new = form.save(commit=False)
            post_new.author = request.user
            post_new.save()
            return super(TopicCreateView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class TopicUpdateView(SuccessMessageMixin, UpdateView):
    """Updating of an existing topic in a forum"""
    model = Topic
    form_class = TopicForm
    template_name = 'posts/topic-edit.html'
    success_url = reverse_lazy('topic_list')
    success_message = _('Тему успішно редаговано')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            topic_new = form.save(commit=False)
            topic_new.author = request.user
            topic_new.save()
            return super(TopicUpdateView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class TopicDeleteView(SuccessMessageMixin, DeleteView):
    """Deleting of an existing topic in a forum"""
    model = Topic
    template_name = 'posts/topic-delete.html'
    success_url = reverse_lazy('topic_list')
    success_message = _('Тему успішно видалено')


class PostListView(FilterView):
    """Listing of posts in a topic"""
    model = Post
    template_name = 'posts/post-list.html'
    paginate_by = 10
    filterset_class = PostFilter
    topic = None

    def get(self, request, *args, **kwargs):
        if self.kwargs['topic'] == None:
            self.topic = Topic.objects.first()
        else:
            self.topic = Topic.objects.get(pk=self.kwargs['topic'])
        return super(PostListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.order_by('-created')
        context['topic'] = self.topic
        return context

    def get_queryset(self):
        return Post.objects.filter(topic=self.topic).order_by('-created')


class PostCreateView(SuccessMessageMixin, CreateView):
    """Creating of a new post in a topic"""
    model = Post
    form_class = PostForm
    form = None
    template_name = 'posts/post-new.html'
    success_message = _('Публікацію успішно створено')

    def get(self, request, *args, **kwargs):
        if self.kwargs['topic'] == None:
            topic = Topic.objects.first()
        else:
            topic = Topic.objects.get(pk=self.kwargs['topic'])
        self.form = PostForm(initial={'topic': topic})
        return super(PostCreateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['topic'] == None:
            topic = Topic.objects.first()
        else:
            topic = Topic.objects.get(pk=self.kwargs['topic'])
        form = PostForm(request.POST)
        if form.is_valid():
            post_new = form.save(commit=False)
            post_new.author = request.user
            post_new.topic = topic
            post_new.save()
            return redirect('post_list', topic=topic.id)
        else:
            return super(PostCreateView, self).get(request, *args, **kwargs)


class PostUpdateView(SuccessMessageMixin, UpdateView):
    """Updating of an existing post in a topic"""
    model = Post
    form_class = PostForm
    template_name = 'posts/post-edit.html'
    success_message = _('Публікацію успішно редаговано')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            post_new = form.save(commit=False)
            post_new.author = request.user
            post_new.save()
            return redirect('post_list', topic=self.kwargs['topic'])
        else:
            return super(PostUpdateView, self).get(request, *args, **kwargs)


class PostDetailView(FormMixin, DetailView):
    """View of details of a post in a topic"""
    model = Post
    template_name = 'posts/post-detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk, 'topic': self.object.topic_id})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        Post.objects.filter(pk=self.object.pk).update(views=F('views') + 1)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object.pk})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            post_comment = form.save(commit=False)
            post_id = form.cleaned_data.get('post')
            content_data = form.cleaned_data.get('content')
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()
            post_comment.post = post_id
            post_comment.content = content_data
            post_comment.parent = parent_obj
            try:
                post_comment.author = request.user
            except:
                post_comment.author = None
            post_comment.save()
            return super(PostDetailView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class PostLikeView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Post, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


class PostDeleteView(SuccessMessageMixin, DeleteView):
    """Deleting of an existing post in a topic"""
    model = Post
    template_name = 'posts/post-delete.html'
    success_message = _('Тему успішно видалено')

    def get_success_url(self):
        return reverse('post_list', kwargs={'topic': self.object.topic_id})
