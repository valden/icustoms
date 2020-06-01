from django.db import models
from user.models import User
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


class Topic(models.Model):
    """Topic model"""
    author = models.ForeignKey(
        User,
        verbose_name=_('Автор'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    title = models.CharField(_('Тема'), max_length=255)
    image = models.ImageField(
        _('Зображення'),
        upload_to='posts/images/',
        null=True,
        blank=True)
    description = models.TextField(
        _('Опис'),
        max_length=255,
        blank=True,
        null=True)
    created = models.DateTimeField(_('Дата створення'), auto_now=True)
    updated = models.DateTimeField(_('Дата редагування'), auto_now=True)
    closed = models.BooleanField(_('Закрита'), blank=True, default=False)

    class Meta:
        verbose_name = _('Тема')
        verbose_name_plural = _('Теми')
        ordering = ('-updated',)

    def __str__(self):
        return self.title

    def get_topic(self):
        return self.pk

    def get_posts(self):
        return self.posts.filter(topic=self.pk)

    def num_posts(self):
        return self.posts.filter(topic=self.pk).count()

    def num_comments(self):
        qs = self.get_posts()
        total_posts = 0
        for post in qs:
            total_posts += int(post.comments.count())
        return total_posts

    def num_views(self):
        qs = self.get_posts()
        total_views = 0
        for post in qs:
            total_views += int(post.views)
        return total_views

    def num_likes(self):
        qs = self.get_posts()
        total_likes = 0
        for post in qs:
            total_likes += int(post.likes.count())
        return total_likes

    def last_post(self):
        if self.posts.count():
            return self.posts.order_by("created")[0]

    def get_absolute_url(self):
        return reverse('post_list', kwargs={'topic': self.id})


class Post(models.Model):
    """Post model"""
    author = models.ForeignKey(
        User,
        verbose_name=_('Автор'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    topic = models.ForeignKey(
        Topic,
        verbose_name=_('Тема'),
        on_delete=models.CASCADE,
        related_name='posts')
    title = models.CharField(_('Заголовок'), max_length=100)
    preview = models.TextField(_('Анонс'), max_length=255)
    image = models.ImageField(
        _('Зображення'),
        upload_to='posts/images/',
        null=True,
        blank=True)
    content = RichTextField(_('Текст публікації'))
    created = models.DateTimeField(_('Дата публікації'), auto_now_add=True)
    updated = models.DateTimeField(_('Дата редагування'), auto_now=True)
    is_published = models.BooleanField(_('Статус публікації'), default=False)
    views = models.IntegerField(
        _('Кількість переглядів'),
        blank=True,
        default=0)
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)

    class Meta:
        verbose_name = _('Публікація')
        verbose_name_plural = _('Публікації')
        ordering = ('-updated',)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.author, self.topic, self.title)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk, 'topic': self.topic_id})

    def get_like_url(self):
        return reverse('post_like', kwargs={'pk': self.pk, 'topic': self.topic_id})


class Comment(models.Model):
    """Comment model"""
    author = models.ForeignKey(
        User,
        verbose_name=_('Автор'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    post = models.ForeignKey(
        Post,
        verbose_name=_('Публікація'),
        on_delete=models.CASCADE,
        related_name='comments')
    parent = models.ForeignKey(
        "self",
        verbose_name=_('Коментар'),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies')
    content = models.TextField(_('Текст коментаря'))
    created = models.DateTimeField(_('Дата створення'), auto_now_add=True)
    updated = models.DateTimeField(_('Дата оновлення'), auto_now=True)

    class Meta:
        verbose_name = _('Коментар')
        verbose_name_plural = _('Коментарі')
        ordering = ('-created',)

    def __str__(self):
        return 'Коментар до публікації "{0}"'.format(self.post.title)

    def replies(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def get_absolute_url(self):
        return reverse('post_detail', args={'pk': self.post.pk, 'topic': self.post.topic_id})
