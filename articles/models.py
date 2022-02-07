from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.conf import settings

from django.utils import timezone
from django.urls import reverse
from .utils import slugify_instance_title

User = settings.AUTH_USER_MODEL


class ArticleQuerySet(models.QuerySet):
    def search(self, search_query=None):
        if search_query is None or search_query == "":
            return self.none()
        lookups = Q(title__icontains=search_query) | Q(
            content__icontains=search_query)
        return self.filter(lookups)


class ArticleManager(models.Manager):
    def get_qeryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search_for_call_in_views_py(self, search_query=None):
        return self.get_qeryset().search(search_query=search_query)


class Article(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(
        default=timezone.now, blank=True, null=True, auto_now=False, auto_now_add=False)

    objects = ArticleManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})


def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)


pre_save.connect(article_pre_save, sender=Article)


def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)


post_save.connect(article_post_save, sender=Article)
