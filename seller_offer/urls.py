from django.urls import path
from .views import showCreateSellerOffer, createSellerOffer, myPostWiseOffers, offeredProdDetails, offersByMe

urlpatterns = [
    path('show-create-seller-offer/<str:post_code_name>', showCreateSellerOffer, name='show-create-seller-offer'),
    path('create-seller-offer', createSellerOffer, name='create-seller-offer'),
    path('my-post-wise-offers/<str:post_code_name>', myPostWiseOffers, name='my-post-wise-offers'),
    path('offered-prod-details/<str:offer_code_name>', offeredProdDetails, name='offered-prod-details'),
    path('offers-by-me', offersByMe, name='offers-by-me')
]