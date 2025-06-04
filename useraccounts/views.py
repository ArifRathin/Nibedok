from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .forms import SignUpForm, LogInForm
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from uuid import uuid4
import json
from . import mail_manager
from useraccounts.tasks import mailer
from django.urls import reverse
from nibedok.ImageManager import getProcessedImage
from django.contrib import messages
# Create your views here.
def signUp(request):
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        print(sign_up_form.is_valid())
        if sign_up_form.is_valid():
            print(sign_up_form.cleaned_data.get('email'))
            first_name = sign_up_form.cleaned_data.get('first_name')
            last_name = sign_up_form.cleaned_data.get('last_name')
            email = sign_up_form.cleaned_data.get('email')
            password = sign_up_form.cleaned_data.get('password')
            with transaction.atomic():
                try:
                    user = User.objects.create_user(email = email, first_name=first_name, last_name=last_name, password=password)
                    user.channel_group_name = f'{uuid4().hex}_{user.id}_23322332'
                    # security_code = mail_manager.genSecurityCode()
                    # print(security_code)
                    # mail_manager.sendSecurityCodeMail(email=email,security_code=security_code,subj="Nibedok Account Verification Email")
                    # user.security_code = user.password
                    # user.set_password(security_code)
                    # user.security_code_generated = True
                    user.save()
                    # mailer.delay(email,security_code,"Nibedok Account Verification Email")
                    # url = reverse('show-verify-account-page',kwargs={'email':email})
                    url = reverse('home',kwargs={'email':email})
                    # print(url)
                    # status = json.dumps({'Success':True, 'url':url})
                    status = json.dumps({'Success':True, 'url':url})
                    return JsonResponse(status, safe=False)
                except Exception as err:
                    print("Error here",str(err))
                    status = json.dumps({'Wrong':err})
                    return JsonResponse(status, safe=False)

        else:
            print(sign_up_form.errors.as_json())
            return JsonResponse(sign_up_form.errors.as_json(), safe=False)
    else:
        sign_up_form = SignUpForm()
    return render(request, 'sign-up.html',{'form':sign_up_form})


def send_verification_code(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            user_exists = User.objects.filter(email=email).exists()
            if not user_exists:
                messages.warning(request, "User doesn't exist!", extra_tags="warning-user")
                return redirect("send-verification-code")
            else:
                user = User.objects.get(email=email)
            security_code = mail_manager.genSecurityCode()
            if user.security_code_generated:
                user.set_password(security_code)
            else:
                user.security_code = user.password
                user.set_password(security_code)
                user.security_code_generated  = True
            user.save()
            mailer.delay(email=email,security_code=security_code,subj="Nibedok Account Verification Email")
            return redirect('show-verify-account-page',email)
        except Exception as e:
            messages.error(request, "Something went wrong!", extra_tags="error")
            return redirect("send-verification-code")
    
    return render(request, 'front-end/send-verification-code.html')


def show_verify_account_page(request, email):
    data = {
        'email_id':email
    }
    return render(request,'front-end/verify-account.html',data)


def verify_account(request):
    try:
        email = request.POST.get('email')
        security_code = request.POST.get('security_code')
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            user = authenticate(email=email,password=security_code)
            if user:
                user_info = User.objects.get(email=email)
                user_info.is_verified = True
                user_info.save()
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, "Account verification failed!", extra_tags="error-verification")
                return redirect('show-verify-account-page',email)
        else:
            messages.warning(request, "Account doesn't exist!", extra_tags="warning-account")
            return redirect("send-verification-code")
    except Exception as e:
        messages.error(request, "Something went wrong!", extra_tags="error")
        return redirect('show-verify-account-page',email)


def logIn(request):
    if request.method == 'POST':
        print("Here")
        logInForm = LogInForm(request.POST)
        if logInForm.is_valid():
            try:
                email = logInForm.cleaned_data['email']
                password = logInForm.cleaned_data['password']
                user_info = User.objects.get(email=email)
                if not user_info.is_verified:
                    status = json.dumps({'Unverified':True})
                    return JsonResponse(status, safe=False)
                if user_info.security_code_generated:
                    user_info.password = user_info.security_code
                    user_info.security_code = None
                    user_info.security_code_generated = False
                    user_info.save()
                        
                user = authenticate(email=email, password=password)
                if user:
                    login(request, user)
                    status = json.dumps({'Success':True})
                    return JsonResponse(status, safe=False)
                else:
                    status = json.dumps({'Invalid':True})
                    return JsonResponse(status, safe=False)
            except Exception as e:
                # status = json.dumps({'Wrong':True})
                status = json.dumps({'Wrong':str(e)})
                return JsonResponse(status, safe=False)
        else:
            return JsonResponse(logInForm.errors.as_json(), safe=False)
    else:
        print('here2')
        logInForm = LogInForm()
    return render(request, 'log-in.html', {'form':logInForm})


def send_password_change_code(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            user_exists = User.objects.filter(email=email)
            if user_exists:
                security_code = mail_manager.genSecurityCode()
                user = User.objects.get(email=email)
                if not user.security_code_generated:
                    user.security_code = user.password
                    user.security_code_generated = True
                user.set_password(security_code)
                user.save()
                mailer.delay(email=email, security_code=security_code, subj="Change Nibedok Password")
                return redirect('show-change-password-page',email)
            else:
                messages.warning(request, "User doesn't exist", extra_tags="warning-user")
                return redirect("send-password-change-code")
        except Exception as e:
            messages.error(request, "Something went wrong!", extra_tags="error")
            return redirect("send-password-change-code")
    return render(request,'front-end/send-password-change-code.html')


def show_change_password_page(request, email):
    data={
        'email':email
    }
    return render(request,'front-end/change-password.html',data)


def change_password(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            user_exists = User.objects.filter(email=email).exists()
            if not user_exists:
                messages.warning(request, "Passwords don't match", extra_tags="warning-email")
                return redirect("send-password-change-code")
            password = request.POST.get('password')
            retype_password = request.POST.get('retype_password')
            if password != retype_password:
                messages.warning(request, "Passwords don't match", extra_tags="warning-password-mismatch")
                return redirect('show-change-password-page',email)
            user = User.objects.get(email=email)
            if not user.security_code_generated:
                messages.warning(request, "Code expired. Please try again.", extra_tags="warning-code-expired")
                return redirect('show-change-password-page',email)
            security_code = request.POST.get('security_code')
            auth = authenticate(email=email,password=security_code)
            if auth:
                user.set_password(password)
                user.security_code = None
                user.security_code_generated = False
                user.save()
                auth_user = authenticate(email=email,password=password)
                if auth_user:
                    login(request,auth_user)
                    return redirect('home')
                messages.error(request, "Authentication failed!", extra_tags="error-auth-failed")
                return redirect('show-change-password-page',email)
            messages.error(request, "Authentication failed!", extra_tags="error-auth-failed")
            return redirect('show-change-password-page',email)
        except Exception as e:
            messages.error(request, "Something went wrong!", extra_tags="error")
            return redirect('show-change-password-page',email)
    

def logOut(request):
    logout(request)
    return redirect('home')


def profile(request, group_name):
    profile = User.objects.get(channel_group_name = group_name)
    data={
        'profile':profile
    }
    return render(request,'front-end/profile.html',data)


def update_profile(request):
    try:
        first_name = request.POST.get('first_name')
        if first_name == '':
            status = json.dumps({'status':'warning', 'message':'First name cannot be empty'})
            return JsonResponse(status,safe=False)
        last_name = request.POST.get('last_name')
        user = User.objects.get(id=request.user.id)
        print("Length: "+str(len(request.FILES)))
        if len(request.FILES) > 1:
            status = json.dumps({'status':'warning', 'message':'Only one photo is allowed'})
            return JsonResponse(status,safe=False)
        if len(request.FILES) > 0:
            photo = request.FILES['profile_photo']
            photo = getProcessedImage(photo)
            user.profile_photo = photo
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        status = json.dumps({'status':'success'})
        return JsonResponse(status,safe=False)
    except Exception as e:
        print(str(e))
        status = json.dumps({'status':'failed'})
        return JsonResponse(status,safe=False)
    

def update_password(request):
    if request.method == 'POST':
        try:
            curr_password = request.POST.get('current_password')
            new_password = request.POST.get("new_password")
            retype_password = request.POST.get("retype_password")
            if curr_password == "" or new_password == "" or retype_password == "":
                messages.warning(request, "No fields can be empty", extra_tags="warning-empty-password")
                return redirect('update-password')
            user = authenticate(email=request.user.email, password=curr_password)
            if not user:
                messages.warning(request, "The current password you entered, is incorrect.", extra_tags="warning-curr-password")
                return redirect('update-password')
            if new_password != retype_password:
                messages.warning(request, "Passwords don't match", extra_tags="warning-password-mismatch")
                return redirect('update-password')
            request.user.set_password(new_password)
            request.user.save()
            user = authenticate(email=request.user.email, password=new_password)
            login(request,user)
            messages.success(request, "Successfully changed password.", extra_tags="success-updated")
            return redirect('update-password')
        except Exception as e:
            messages.error(request, "Something went wrong.", extra_tags="failed")
            return redirect('update-password')
    return render(request, 'front-end/update-password.html')