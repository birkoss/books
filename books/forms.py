from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import LibraryTemplate


class LibraryForm(forms.Form):
	error_css_class = "alert alert-danger"

	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	template = forms.ModelChoiceField(queryset=LibraryTemplate.objects.all())

	def clean_name(self):
		data = self.cleaned_data['name']

		if data == "error":
			raise ValidationError(_('Validation Error !!'))

		return data


class LibraryCategoryForm(forms.Form):
	error_css_class = "alert alert-danger"

	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))


class BookForm(forms.Form):
	error_css_class = "alert alert-danger"

	name = forms.CharField(label='Nom du livre', widget=forms.TextInput(attrs={'class':'form-control'}))
	url = forms.CharField(label='URL', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
	cover = forms.CharField(label='Image de la pochette', required=False, widget=forms.FileInput(attrs={'class':'form-control image-input', 'accept': 'image/*', 'multiple': 'multiple'}))

	def clean_url(self):
		data = self.cleaned_data['url']

		if data:
			if data[0:7] != "http://" and data[0:8] != "https://":
				raise ValidationError(_("L'URL doit commencer par http:// ou https://"))

		return data

