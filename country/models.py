from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField('useraccounts.User', related_name='countries')

    def __str__(self):
        return self.name
    

class Currency(models.Model):
    code = models.CharField(10)
    name = models.CharField(100)

    def __str__(self):
        return f'{self.name}({self.code})'