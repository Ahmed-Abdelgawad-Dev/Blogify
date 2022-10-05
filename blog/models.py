from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

INF_TIME = datetime.max.replace(tzinfo=timezone.utc)


def get_inf_time():
	return INF_TIME


class Post(models.Model):
	class Status(models.TextChoices):
		DRAFT = 'DF', 'Draft'
		PUBLISHED = 'PB', 'Published'

	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
	body = models.TextField()
	publish = models.DateTimeField(default=get_inf_time)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

	class Meta:
		ordering = ['-publish']
		indexes = [models.Index(fields=['-publish']), ]

	def __str__(self):
		return self.title
