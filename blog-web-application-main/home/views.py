from django.shortcuts import render, redirect
from .form import *
from django.contrib.auth import logout
from .twilio import otp_created
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
import json




def logout_view(request):
    logout(request)
    return redirect('/')


def home(request):
    context = {'blogs': BlogModel.objects.all()}
    return render(request, 'home.html', context)


def login_view(request):
    return render(request, 'login.html')

@login_required
def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html', context)

@login_required
def see_blog(request):
    context = {}

    try:
        blog_objs = BlogModel.objects.filter(user=request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)

    print(context)
    return render(request, 'see_blog.html', context)

@login_required
def add_blog(request):
    context = {'form': BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES.get('image', '')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                print('Valid')
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user=user, title=title,
                content=content, image=image
            )
            print(blog_obj)
            return redirect('/add-blog/')
    except Exception as e:
        print(e)

    return render(request, 'add_blog.html', context)

@login_required
def blog_update(request, slug):
    context = {}
    try:

        blog_obj = BlogModel.objects.get(slug=slug)

        if blog_obj.user != request.user:
            return redirect('/')

        initial_dict = {'content': blog_obj.content}
        form = BlogForm(initial=initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user=user, title=title,
                content=content, image=image
            )

        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'update_blog.html', context)

@login_required
def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)

        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e:
        print(e)

    return redirect('/see-blog/')


def register_view(request):
    return render(request, 'register.html')


def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
        return redirect('/login/')

    except Exception as e:
        print(e)

    return redirect('/')

def reset_password_page(request):

    if request.method == 'POST':
        context = {}
        email = request.POST.get('email')
        subject = 'Password Reset Request'
        message = 'Please verify your Otp'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        form = ResetModel(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            new_password = form.cleaned_data['new_password']
            user = User.objects.filter(email=email).first()
            user.set_password(new_password)
            user.save()
            otp = otp_created(mobile=mobile)
            number = MobileModel.objects.create(user=user, mobile=mobile, otp=otp)
            number.save()
            id = user.id
            messages = "Reset Password Successfully"
            print(messages)
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            url = f'/otp/{id}'
            return redirect(url)
    else:
        form = ResetModel()
    return render(request, 'reset_password.html', {'form': form})


def otp_page(request, id=None):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_check=  MobileModel.objects.filter(user_id=id, otp=otp)
        if otp_check:
            return redirect('/thank-you/')
        else:
            return render(request, 'otp.html', {'message':'Please Enter Correct Otp'})

    return render(request, 'otp.html')


def thsnk_you_page(request):
    return render(request , 'thank_you.html')

class UserEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.username
        return super().default(obj)

def suspened_page(request):
    if request.method == 'POST':
        toggle_value = request.POST.get("is_on")
        if toggle_value == 'true':
            username = request.POST.get("email_list")
            try:
                check_user = User.objects.get(username=username)
                id = check_user.id
                user = check_user.is_superuser
                if check_user.username and user == False:
                    checkuser = CustomModel.objects.get(user_id = id)
                    if checkuser:
                        CustomModel.objects.filter(user_id=id).update(is_pass_change=True)
                    else:
                        checkuser = CustomModel.objects.create(user_id = id, is_pass_change=True)
            except User.DoesNotExist:
                pass
            
            message =  username + ' Your are  Suspended'
            context = {
                'message': message, 
                'username':check_user,
                'Email':check_user
            }
            json_data = json.dumps(context, cls=UserEncoder)
            return JsonResponse(json_data, safe=False)

  
        else:
            username = request.POST.get("email_list")
            try:
                check_user = User.objects.get(username=username)
                id = check_user.id
                user = check_user.is_superuser
                if check_user.username and user == False:
                    checkuser = CustomModel.objects.get(user_id = id)
                    if checkuser:
                        CustomModel.objects.filter(user_id=id).update(is_pass_change=False)
                    else:
                        checkuser = CustomModel.objects.create(user_id = id, is_pass_change=False)

            except User.DoesNotExist:
                pass
            message = username + ' Your are not  Suspended'
            context = {
                'message': message, 
                'username':check_user,
                'Email':check_user
            }
            json_data = json.dumps(context, cls=UserEncoder)
            return JsonResponse(json_data, safe=False)

    else:
        all_users = User.objects.all()
        return render(request, 'suspened.html', {'all': all_users})



def user_profile(request):
    if request.method == 'GET':
        all_users = User.objects.all()
        context = {'user': all_users}
        return render(request, context)





