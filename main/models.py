from django.db import models
import uuid


class Product(models.Model):

    CATEGORY_CHOICES = [
        ('footwear', 'Footwear'),
        ('kit', 'Kit'),
        ('shorts and pants', 'Shorts and Pants'),
        ('jackets and sportswear', 'Jackets and Sportswear'),
        ('tracksuits', 'Tracksuits'),
        ('others', 'Others'),
    ]
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    # brand = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @property
    def is_product_featured(self):
        return self.is_featured

    def increment_views(self):
        self.views += 1
        self.save()
