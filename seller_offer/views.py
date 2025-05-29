from django.shortcuts import render, HttpResponse, redirect
# from .forms import CreateOfferForm, SamplePhotoForm
from buyer_post.models import BuyerPost
from .models import SellerOffer, SellerSamplePhoto
from notification.models import NotificationType, Notification
from country.models import Currency
from django.db import transaction
from django.core.files.base import ContentFile
import base64
from nibedok.ImageManager import getProcessedImage
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings
from datetime import datetime
from uuid import uuid4
# Create your views here.
def showCreateSellerOffer(request, post_code_name):
    offers_count_today = SellerOffer.objects.filter(user=request.user,created_at__contains=datetime.today().date()).count()
    if offers_count_today >= 3:
        return render(request, 'front-end/offer-limit.html')
    buyer_post_exists = BuyerPost.objects.filter(post_code_name=post_code_name).exists()
    if buyer_post_exists:
        buyer_post = BuyerPost.objects.get(post_code_name=post_code_name)
        currencies = Currency.objects.all()
        return render(request,'front-end/create-seller-offer.html',{'buyer_post':buyer_post,'currencies':currencies})


def createSellerOffer(request):
    offers_count_today = SellerOffer.objects.filter(user=request.user,created_at__contains=datetime.today().date()).count()
    if offers_count_today >= 3:
        return render(request, 'front-end/offer-limit.html')
    if request.method == 'POST':
        try:
            post_code_name = request.POST.get('post_code_name')
            post_exists = BuyerPost.objects.filter(post_code_name=post_code_name).exists()
            if not post_exists:
                messages.warning(request,"Post doesn't exist.",extra_tags="warning-post")
                return redirect("show-create-seller-offer",post_code_name)
            buyer_post = BuyerPost.objects.get(post_code_name=post_code_name)
            offer_msg = request.POST.get('offer_msg')
            if offer_msg == '' or len(offer_msg) > 1000:
                messages.warning(request, "Message cannot be empty or exceed 1000 letters", extra_tags="warning-msg-len")
                return redirect("show-create-seller-offer",post_code_name)
            offer_msg = offer_msg.strip()
            estimated_delivery_time = int(request.POST.get('estimated_delivery_time'))
            if estimated_delivery_time < 1:
                messages.warning(request, "Delivery time has to be 1 day or more.", extra_tags="warning-delivery-time")
                return redirect("show-create-seller-offer",post_code_name)
            price = int(request.POST.get('price'))
            if price<0:
                messages.warning(request,"Price has to be a positive number", extra_tags="warning-price")
                return redirect("show-create-seller-offer",post_code_name)
            currency_id = request.POST.get('currency_id')
            currency_exists = Currency.objects.filter(id=currency_id).exists()
            if not currency_exists:
                messages.warning(request, "Please insert a valid currency", extra_tags="warning-currency")
                return redirect("show-create-seller-offer",post_code_name)
            with transaction.atomic():
                seller_offer = SellerOffer.objects.create(user=request.user, currency_id=currency_id, buyer_post_id=buyer_post.id, post_code_name=buyer_post.post_code_name, offer_msg=offer_msg, estimated_delivery_time=estimated_delivery_time, price=price)
                seller_offer.offer_code_name = f'{uuid4().hex}_23{seller_offer.id}_232332'
                seller_offer.save()
                photo_list = []
                photo_strs = request.POST.getlist('img-str')
                if len(photo_strs) > 5:
                    messages.warning(request,"At most 5 photos can be uploaded",extra_tags='warning-photo-len')
                    return redirect('show-create-seller-offer',post_code_name)
                for photo_str in photo_strs:
                    format, img_str = photo_str.split(';base64,')
                    extension = format.split('/')[-1]
                    if extension != 'jpeg' and extension != 'jpg' and extension != 'JPEG' and extension != 'JPG' and extension != 'png' and extension != 'PNG':
                        messages.warning(request,"Photo has to be either JPG/PNG", extra_tags='warning-photo-format')
                        return redirect('show-create-seller-offer',{'post_code_name':post_code_name})
                    photo = ContentFile(base64.b64decode(img_str), name='tmp.'+extension)
                    if photo.size > settings.MAX_UPLOAD_LIMIT:
                        messages.warning(request,"A photo cannot be more than 3MB!", extra_tags='warning-photo-size')
                        return redirect('show-create-seller-offer',post_code_name)
                    photo = getProcessedImage(photo)
                    tmp = SellerSamplePhoto(seller_offer=seller_offer,photo=photo)
                    photo_list.append(tmp)
                SellerSamplePhoto.objects.bulk_create(photo_list)
                notif_type = NotificationType.objects.get(name='got_offer')
                notif_exists = Notification.objects.filter(post_code_name=post_code_name, type=notif_type).exists()
                if notif_exists:
                    notif = Notification.objects.get(post_code_name=post_code_name, type=notif_type)
                    notif.notif_for = seller_offer.buyer_post.user
                    notif.post_code_name = seller_offer.buyer_post.post_code_name
                    notif.notif_msg = ""+request.user.first_name.capitalize()+" "+request.user.last_name.capitalize()+" and "+str(notif.total_offers)+" other want to show you their products."
                    notif.if_read = False
                    notif.total_offers += 1
                    notif.save()
                else:
                    notif_msg = ""+request.user.first_name.capitalize()+" "+request.user.last_name.capitalize()+" wants to show you their products"
                    Notification.objects.create(post_code_name=post_code_name,notif_for=seller_offer.buyer_post.user,type=notif_type,notif_msg=notif_msg,total_offers=1)
                messages.success(request,"Successfully sent!", extra_tags="success-sent")
                return redirect("show-create-seller-offer",post_code_name)
        except Exception as e:
            # return HttpResponse(str(e))
            messages.error(request, "Something went wrong. Please check your input values.", extra_tags="failed")
            return redirect("show-create-seller-offer",post_code_name)
        

def myPostWiseOffers(request, post_code_name):
    buyer_post = BuyerPost.objects.get(post_code_name=post_code_name)
    seller_offers = SellerOffer.objects.filter(post_code_name=post_code_name)
    data = {
        'buyer_post':buyer_post,
        'seller_offers':seller_offers,
    }
    return render(request, 'front-end/my-post-wise-offers.html', data)
    return render(request, 'my-post-wise-offers.html', data)


def offeredProdDetails(request, offer_code_name):
    try:
        offer = SellerOffer.objects.get(offer_code_name=offer_code_name)
        data = {
            'offer':offer
        }
        return render(request, 'front-end/offered-product-details.html', data)
    except Exception as e:
        return render(request,'front-end/error-page.html')


def offersByMe(request):
    paginated = Paginator(SellerOffer.objects.filter(user=request.user).order_by('-created_at'),10)
    page = request.GET.get('page')
    offers = paginated.get_page(page)
    data={
        'offers':offers
    }
    return render(request,'front-end/offers-by-me.html',data)