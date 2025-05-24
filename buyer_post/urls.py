from django.urls import path
from .views import createBuyerPost, showMyPosts, buyerPostDetails, publishingPost, deletePost
urlpatterns = [
    path('create-buyer-post', createBuyerPost, name='create-buyer-post'),
    path('show-my-posts', showMyPosts, name='show-my-posts'),
    path('buyer-post-details/<str:post_code_name>', buyerPostDetails, name='buyer-post-details'),
    path('publishing-post/<str:post_code_name>', publishingPost, name='publishing-post'),
    path('delete-post/<str:post_code_name>', deletePost, name='delete-post')
]