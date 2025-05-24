"""
URL configuration for nibedok project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import index, prodsByCat, searchResultsSuggestions, searchResults
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='home'),
    path('prods-by-cat/<slug:slug>',prodsByCat,name='prods-by-cat'),
    path('search-results-suggestions/',searchResultsSuggestions,name='search-results-suggestions'),
    path('search-results',searchResults,name='search-results'),
    path('country/',include('country.urls')),
    path('user-accounts/',include('useraccounts.urls')),
    path('buyer-post/',include('buyer_post.urls')),
    path('seller-offer/',include('seller_offer.urls')),
    path('inbox/',include('inbox.urls')),
    path('notifications/',include('notification.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)