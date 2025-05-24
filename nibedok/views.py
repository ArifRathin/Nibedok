from django.shortcuts import render,HttpResponse
from buyer_post.models import BuyerPost
from product.models import ProductCategory
from notification.models import NotificationType, Notification
from seller_offer.models import SellerOffer
from useraccounts.forms import SignUpForm, LogInForm
from datetime import date, timedelta
from django.db.models import F, Q
import json
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator

def index(request):
    posts = getPostsByProdCat(request, 'all-categories')
    sign_up_form = SignUpForm()
    log_in_form = LogInForm()
    categories = ProductCategory.objects.all()
    # notifications = []
    # if request.user.is_authenticated:
    #     notif_exists = Notification.objects.filter(notif_for=request.user).exists()
    #     if notif_exists:
    #         notifications = Notification.objects.filter(notif_for=request.user)
    data = {
        'posts':posts,
        'sign_up_form':sign_up_form,
        'log_in_form':log_in_form,
        'categories':categories,
        'slug':'all-categories',
        # 'notifications':notifications,
        'env':'home'
    }
    return render(request,'front-end/home.html',data)
    return render(request,'index.html',data)


def getPostsByProdCat(request, slug):
    posts_already_shown_prod = []
    if request.user.is_authenticated:
        if_exists = SellerOffer.objects.filter(user_id=request.user.id).exists()
        if if_exists:
            user_offers = SellerOffer.objects.filter(user_id=request.user.id)
            for offer in user_offers:
                posts_already_shown_prod.append(offer.buyer_post_id)
    if slug == 'all-categories': 
        if len(posts_already_shown_prod) > 0:
            posts = BuyerPost.objects.filter(~Q(id__in=posts_already_shown_prod),if_published=True,created_at__gte=date.today()-timedelta(days=1)*F('deadline')).order_by('?')[:10]
        else:
            posts = BuyerPost.objects.filter(if_published=True,created_at__gte=date.today()-timedelta(days=1)*F('deadline')).order_by('?')[:10]
    else:
        cat_row = ProductCategory.objects.get(slug=slug)
        ids = []
        ids.append(cat_row.id)
        if len(posts_already_shown_prod) > 0:
            posts = BuyerPost.objects.filter(~Q(id__in = posts_already_shown_prod),product_categories__in=ids,if_published=True,created_at__gte=date.today()-timedelta(days=1)*F('deadline')).order_by('?')[:10]
        else:
            posts = BuyerPost.objects.filter(product_categories__in=ids,if_published=True,created_at__gte=date.today()-timedelta(days=1)*F('deadline')).order_by('?')[:10]
    return posts


def prodsByCat(request, slug):
    posts = getPostsByProdCat(request,slug)
    sign_up_form = SignUpForm()
    log_in_form = LogInForm()
    categories = ProductCategory.objects.all()
    data = {
        'posts':posts,
        'sign_up_form':sign_up_form,
        'log_in_form':log_in_form,
        'categories':categories,
        'slug':slug
    }
    return render(request,'front-end/home.html',data)


def searchResultsSuggestions(request):
    keywords = request.GET.get('keywords')
    search_results = BuyerPost.objects.filter(Q(description__icontains=keywords)|Q(title__icontains=keywords),if_published=True,created_at__gte=date.today()-timedelta(1)*F('deadline')).distinct('id')[:5]
    search_results_list = []
    for result in search_results:
        search_results_list.append({'url':reverse('buyer-post-details',kwargs={'post_code_name':result.post_code_name}),'title':result.title})
    data = {
        'results':search_results_list
    }
    results = json.dumps(data)
    return JsonResponse(results, safe=False)


def searchResults(request):
    keywords = request.GET.get('keywords')
    paginated = Paginator(BuyerPost.objects.filter(Q(description__icontains=keywords)|Q(title__icontains=keywords),if_published=True,created_at__gte=date.today()-timedelta(1)*F('deadline')), 10)
    page = request.GET.get('page')
    search_results = paginated.get_page(page)
    data = {
        'search_results':search_results
    }
    return render(request, 'front-end/search-results.html', data)