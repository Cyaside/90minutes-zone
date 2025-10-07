from django import forms
from django.forms import ModelForm
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from urllib.parse import urlparse

from main.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'description',
            'thumbnail',
            'category',
            'is_featured',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ini buat Apply Tailwind CSS classes to all form fields
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-gray-100 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-black focus:border-black transition'
            })

    def clean_name(self):
        name = strip_tags(self.cleaned_data.get('name', '')).strip()
        if not name:
            raise ValidationError('Name is required.')
        return name

    def clean_description(self):
        description = strip_tags(self.cleaned_data.get('description', '')).strip()
        if not description:
            raise ValidationError('Description is required.')
        return description

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        if not thumbnail:
            return thumbnail  # allow blank
        parsed = urlparse(thumbnail)
        if parsed.scheme.lower() not in ('http', 'https') or not parsed.netloc:
            raise ValidationError('Thumbnail must be a valid http/https URL.')
        if len(thumbnail) > 500:
            raise ValidationError('Thumbnail URL too long (max 500 chars).')
        return thumbnail

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category not in dict(Product.CATEGORY_CHOICES):
            raise ValidationError('Invalid category.')
        return category

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise ValidationError('Price is required.')
        if price < 0:
            raise ValidationError('Price must be non-negative.')
        return price

        