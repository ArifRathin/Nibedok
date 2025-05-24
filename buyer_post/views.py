from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import BuyerPostForm, SamplePhotoForm
# from product.forms import ProductCategoriesForm
from .models import BuyerPost, BuyerSamplePhoto
from notification.models import Notification
from product.models import ProductCategory
from django.db import transaction
from django.core.files.base import ContentFile
import base64
from django.http import JsonResponse
from nibedok.ImageManager import getProcessedImage
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from uuid import uuid4
# Create your views here.
@login_required(login_url='log-in')
def createBuyerPost(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            if len(title) > 100:
                messages.warning(request,"Title cannot exceed 100 characters.",extra_tags='warning-title')
                return redirect('create-buyer-post')
            deadline = int(request.POST.get('deadline'))
            if deadline < 1 or deadline > 60:
                messages.warning(request,"Deadline has to be within 1-60 days.",extra_tags='warning-deadline')
                return redirect('create-buyer-post')
            description = request.POST.get('description')
            if len(description) > 250:
                messages.warning(request,"Description cannot exceed 250 characters.",extra_tags='warning-description')
                return redirect('create-buyer-post')
            category = int(request.POST.get('category'))
            if category < 1:
                messages.warning(request,"Category doesn't exist.",extra_tags='warning-category')
                return redirect('create-buyer-post')
            cat_exists = ProductCategory.objects.filter(id=category).exists()
            if not cat_exists:
                messages.warning(request,"Category doesn't exist.",extra_tags='warning-category')
                return redirect('create-buyer-post')
            with transaction.atomic():
                buyerPost = BuyerPost.objects.create(user=request.user,title=title,deadline=deadline,description=description)
                categories = []
                categories.append(request.POST.get('category'))
                buyerPost.product_categories.set(categories)
                buyerPost.save()
                buyerPost.post_code_name = f'{uuid4().hex}_23{buyerPost.id}_232332'
                buyerPost.save()
                photo_list = []
                img_strs = request.POST.getlist('img-str')
                if len(img_strs) > 5:
                    messages.warning(request,"At most 5 photos can be uploaded",extra_tags='warning-img')
                    return redirect('create-buyer-post')
                for img_str in img_strs:
                    format, imgstr = img_str.split(';base64,')
                    extension = format.split('/')[-1]
                    if extension != 'jpeg' and extension != 'jpg' and extension != 'JPEG' and extension != 'JPG' and extension != 'png' and extension != 'PNG':
                        messages.warning(request,"Image has to be either JPG/PNG", extra_tags='warning-img')
                        return redirect('create-buyer-post')
                    photo = ContentFile(base64.b64decode(imgstr),name='tmp.'+extension)
                    if photo.size > settings.MAX_UPLOAD_LIMIT:
                        messages.warning(request,"An image cannot be more than 3MB!", extra_tags='warning-img')
                        return redirect('create-buyer-post')
                    photo = getProcessedImage(photo)
                    photo_list.append(BuyerSamplePhoto(post=buyerPost,photo=photo))
                BuyerSamplePhoto.objects.bulk_create(photo_list)
                messages.success(request,"Successfully posted!", extra_tags='success')
                return redirect('create-buyer-post')
        except Exception as e:
           messages.error(request,"Could not post. Please try again.", extra_tags='failed')
           return redirect('create-buyer-post')
    else:
        categories = ProductCategory.objects.all()
    return render(request, 'front-end/create-buyer-post.html', {'categories':categories})
    return render(request, 'create-buyer-post.html', {'sample_photo_form':samplePhotoForm,'create_form':createForm, 'prod_cat_form':prodCatForm})


def showMyPosts(request):
    paginated = Paginator(BuyerPost.objects.filter(user=request.user).order_by('-created_at'),10)
    page = request.GET.get('page')
    my_posts = paginated.get_page(page)
    # my_posts = BuyerPost.objects.filter(user=request.user).order_by('-created_at')
    data = {
        'my_posts':my_posts
    }
    return render(request,'front-end/show-my-posts.html',data)
    return render(request,'my-posts.html',data)


def buyerPostDetails(request, post_code_name):
    try:
        buyer_post = BuyerPost.objects.get(post_code_name=post_code_name)
        data = {
            'buyer_post':buyer_post
        }
        return render(request,'front-end/buyer-post-details.html',data)
    except Exception as e:
        return render(request,'front-end/error-page.html')

def publishingPost(request, post_code_name):
    try:
        buyer_post = BuyerPost.objects.get(post_code_name=post_code_name)
        buyer_post.if_published = not buyer_post.if_published
        buyer_post.save()
        return JsonResponse(buyer_post.if_published,safe=False)
    except:
        return JsonResponse(buyer_post.if_published,safe=False)
def deletePost(request, post_code_name):
    try:
        with transaction.atomic():
            buyer_post = BuyerPost.objects.get(post_code_name=post_code_name)
            buyer_post.delete()
            notification = Notification.objects.get(post_code_name=post_code_name)
            notification.delete()
        return JsonResponse('success',safe=False)
    except:
        return JsonResponse('failed',safe=False)