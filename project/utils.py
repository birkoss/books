import os
import itertools
import random
import string

from django.db import models
from django.utils.text import slugify

from project.config import MEDIA_ROOT, MEDIA_URL

def get_existing_image(image_field):
	image = None

	if image_field:
		image_filename = MEDIA_ROOT + "/" + image_field.url.replace(MEDIA_URL, "")
		if os.path.isfile(image_filename):
			image = image_field

	return image


def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def md5ify_model(model: models.Model) -> str:
	slug_candidate = slug_original = generate_random_string(8)

	for i in itertools.count(1):
		if not model.objects.filter(slug=slug_candidate).exists():
			break
		slug_candidate = generate_random_string(8)

	return slug_candidate


def slugify_model(model: models.Model, content: str) -> str:
	slug_candidate = slug_original = slugify(content)

	for i in itertools.count(1):
		if not model.objects.filter(slug=slug_candidate).exists():
			break
		slug_candidate = '{}-{}'.format(slug_original, i)

	return slug_candidate