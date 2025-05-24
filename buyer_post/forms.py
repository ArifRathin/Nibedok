from django import forms
from .models import BuyerPost, BuyerSamplePhoto

class BuyerPostForm(forms.ModelForm):
    class Meta:
        model = BuyerPost
        fields = ['country','title','description','state_district','deadline']
        label = {'country':'','title':'','description':'','state_district':'',}
    

class SamplePhotoForm(forms.ModelForm):
    class Meta:
        model = BuyerSamplePhoto
        fields = ['photo']