from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default=None, null=True)
    users = models.ManyToManyField('useraccounts.User',related_name='productCategories')


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug