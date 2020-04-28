from django.db import models
from django.utils.translation import ugettext_lazy as _


class News(models.Model):
    publisher = models.CharField(max_length=255)
    url = models.URLField()
    rss_url = models.URLField()
    date_format = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True, help_text='Enter tags for search using whitespaces between')

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
        ordering = ('publisher',)

    def __str__(self):
        return self.publisher
    


