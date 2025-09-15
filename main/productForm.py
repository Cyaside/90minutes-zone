from django.forms import ModelForm
from main.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'thumbnail', 'category', 'is_featured']

    # Tailwind Classes ke Widget gegara django gak bisa calling methods dengan keyword arguments
    # biar gak lupa
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ini buat Apply Tailwind CSS classes to all form fields
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-gray-100 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-black focus:border-black transition'
            })

        