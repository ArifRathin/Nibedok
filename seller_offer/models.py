from django.db import models
from useraccounts.models import User
from country.models import Currency
from buyer_post.models import BuyerPost
import os
from uuid import uuid4
# Create your models here.
class SellerOffer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    buyer_post = models.ForeignKey(BuyerPost, on_delete=models.CASCADE)
    post_code_name = models.CharField(default=None, null=True, max_length=250)
    offer_msg = models.TextField()
    offer_code_name = models.CharField(default=None, null=True, max_length=250)
    estimated_delivery_time = models.IntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def photos(self):
        return self.sellersamplephoto_set.filter(seller_offer_id = self.id)


def saveSamplePhoto(instance, filename):
    extension = filename.split('.')[-1]
    if instance.pk:
        filename = f'{instance.pk}{uuid4().hex}.{extension}'
    else:
        filename = f'{uuid4().hex}.{extension}'
    return os.path.join('seller_sample_photos',filename)


class SellerSamplePhoto(models.Model):
    seller_offer = models.ForeignKey(SellerOffer, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=saveSamplePhoto)
