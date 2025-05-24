from django import forms
from .models import SellerOffer, SellerSamplePhoto

class CreateOfferForm(forms.ModelForm):
    class Meta:
        model = SellerOffer
        fields = ['offer_msg','estimated_delivery_time','price','currency']


class SamplePhotoForm(forms.ModelForm):
    class Meta:
        model = SellerSamplePhoto
        fields = ['photo']