from django import forms
from .models import ProductCategory

# class ProductCategoriesForm(forms.ModelForm):
#     class Meta:
#         model=ProductCategory
#         fields = ['name']
#         CHOICES = []
#         for c in ProductCategory.objects.all():
#             tmp = (c.id, c.name)
#             CHOICES.append(tmp)
#         # print(CHOICES)
#         widgets = {
#             'name':forms.Select(choices=CHOICES)
#         }
#         labels = {
#             'name':'Product categories'
#         }