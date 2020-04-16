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