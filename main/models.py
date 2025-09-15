from django.db import models
import uuid


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def is_product_featured(self):
        return self.is_featured

    # def increment_views(self):
    #     self.product_views += 1
    #     self.save()
