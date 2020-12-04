from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    objects = models.Manager()  # The default manage
    published = PublishedManager()  # Out custom manager
    title = models.CharField(_("Title"), max_length=250)
    slug = models.SlugField(_("Slug"), max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name='blog_post')
    body = models.TextField(_("Body"))
    publish = models.DateTimeField(_("Publish"), default=timezone.now)
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)
    status = models.CharField(_("Status"), max_length=10, choices=STATUS_CHOICES, default='draft')


    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", 
                                        args=[self.publish.year,
                                        self.publish.month,
                                        self.publish.day, self.slug])
    



