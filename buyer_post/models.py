from django.db import models
from country.models import Country
from useraccounts.models import User
from uuid import uuid4
import os
from django.urls import reverse

# Create your models here.
class BuyerPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=None, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    post_code_name = models.CharField(default=None, null=True, max_length=250)
    state_district = models.CharField(max_length=250, default=None, null=True)
    deadline = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    if_published = models.BooleanField(default=True)
    product_categories = models.ManyToManyField('product.ProductCategory', related_name='buyerPosts')

    def __str__(self):
        return self.title
    
    def sample_photos(self):
        return self.buyersamplephoto_set.filter(post_id=self.id)

    def offer_count(self):
        return self.selleroffer_set.filter(buyer_post_id=self.id).count()

    def publishing_url(self):
        return reverse('publishing-post',kwargs={'post_code_name':self.post_code_name})

    def delete_url(self):
        return reverse('delete-post',kwargs={'post_code_name':self.post_code_name})


def saveSamplePhoto(instance, filename):
    extension = filename.split('.')[-1]
    if instance.pk:
        filename = f'{instance.pk}{uuid4().hex}.{extension}'
    else:
        filename = f'{uuid4().hex}.{extension}'
    return os.path.join('buyer_sample_photos',filename)


class BuyerSamplePhoto(models.Model):
    post = models.ForeignKey(BuyerPost, on_delete=models.CASCADE, default=None, null=True)
    photo = models.ImageField(upload_to=saveSamplePhoto)