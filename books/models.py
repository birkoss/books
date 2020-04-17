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
	active = models.BooleanField(default=False)

	def __str__(self):
		return self.name + " - " + self.user.username

	def save(self, *args, **kwargs):
		if not self.slug.strip():
			self.slug = md5ify_model(self.__class__)
		super().save(args, kwargs)


class LibraryCategory(models.Model):
	name = models.CharField(max_length=200, default='')
	library = models.ForeignKey(Library, blank=True, null=True, on_delete=models.PROTECT)
	active = models.BooleanField(default=False)
	order = models.IntegerField(default=0, null=True)

	class Meta:
		ordering = ('order', )

	def __str__(self):
		return self.name# + " - " + self.library.name

	def save(self, *args, **kwargs):
		if self.order == 0:
			 category = LibraryCategory.objects.filter(library=self.library).order_by("-order").first()
			 if category is not None:
			 	self.order = category.order + 1
			 else:
			 	self.order = 1
		super().save(args, kwargs)


class Book(models.Model):
	name = models.CharField(max_length=200, default='')
	url = models.CharField(max_length=300, default='')
	category = models.ForeignKey(LibraryCategory, blank=True, null=True, on_delete=models.PROTECT)
	cover = models.ImageField(null=True)

