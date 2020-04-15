from django.contrib.auth.models import User
from django.db import models


from project.utils import md5ify_model, slugify_model


class LibraryTemplate(models.Model):
	name = models.CharField(max_length=100, default='')
	slug = models.CharField(max_length=100, blank=True, default='')

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug.strip():
			self.slug = slugify_model(self.__class__, self.__str__())
		super().save(args, kwargs)


class Library(models.Model):
	name = models.CharField(max_length=200, default='')
	slug = models.CharField(max_length=8, blank=True, default='')
	template = models.ForeignKey(LibraryTemplate, blank=True, null=True, on_delete=models.PROTECT)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)

	def __str__(self):
		return self.name + " - " + self.user.username

	def save(self, *args, **kwargs):
		if not self.slug.strip():
			self.slug = md5ify_model(self.__class__)
		super().save(args, kwargs)