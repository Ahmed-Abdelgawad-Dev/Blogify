from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


def get_inf_time():
    return timezone.now()


class PublishedManager(models.Manager):
    """Published Posts' Manager"""

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=255)
    # Unique for the date ONLY not for the time.
    slug   = models.SlugField(max_length=255, unique_for_date='publish')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    body    = models.TextField()
    publish = models.DateTimeField(default=get_inf_time)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status  = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects   = models.Manager()  # Default Manager
    published = PublishedManager()  # CustomModel Manager

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish']), ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[
            self.publish.year, self.publish.month,
            self.publish.day, self.slug
        ])
