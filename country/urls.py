from django.urls import path
from .views import populateCountriesTable, populateCurrenciesTable

urlpatterns = [
    path('populate-countries-table', populateCountriesTable, name='populate-countries-table'),
    path('populate-currencies-table', populateCurrenciesTable, name='populate-currencies-table')
]