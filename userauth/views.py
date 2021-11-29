
# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect
# from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import auth_login as default_login

from django.template.loader import render_to_string, get_template
# from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
# from django.views import View
# from userauth.forms import LoginForm
# from django.contrib.auth.forms import AuthenticationForm
from .forms import AuthenticationForm
from .token import account_activation_token
# from django.contrib.auth.models import User
from .models import User, UserProfile
from django.contrib.auth.views import auth_logout
from .forms import RegisterForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, JsonResponse
import stripe


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


import json



def home(request):
    return render(request, template_name='home.html')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_active = 1
            email = form.cleaned_data.get('email', "")
            password = form.cleaned_data.get('password', "")
            password2 = form.cleaned_data.get('password2', "")
            user.set_password(password)
            first_name = form.cleaned_data.get('first_name', "")
            last_name = form.cleaned_data.get('last_name', "")
            user.username = first_name + "_" + last_name
            user.save()

            location = form.cleaned_data.get('location', "")
            phone_number = form.cleaned_data.get('phone_number', "")
            profile_photo = form.cleaned_data.get('profile_photo', "")
            user_profile = UserProfile(user=user, last_name=last_name, first_name=first_name, location=location, phone_number=phone_number, avatar=profile_photo)
            user_profile.save(user)
            # return redirect("account_activation_sent")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, template_name="singup.html", context={'form': form})




from django.views.generic import TemplateView

class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


def success(request):
    return render(request, 'success.html')


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


def logout(request):
    # if request.method == 'POST':
    print(" inside post")
    auth_logout(request)
    return redirect('home')


def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

    return None

"""
def login_view(request):
    print(' request.body ', request.method)
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        print('form  ', form.is_valid())
        print(form.errors)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate_user(email, password)
            context = {}

            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect('home')
                else:
                    context['error_message'] = "user is not active"
            else:
                context['error_message'] = "email or password not correct"

            return redirect('login')
        messages.error(request, 'Please provide valid credentials')
        return redirect('login')
    else:
        form = AuthenticationForm()
        return render(request, template_name="login.html", context={'form': form})
"""

def  login_view(request):
    """
      Renders Login Form
    """
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        form    = AuthenticationForm(request.POST)
        email   = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate_user(email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged In")
            return redirect("home")
        else:

            messages.error(request, "please Correct Below Errors")
    else:
        form = AuthenticationForm()

    return render(request, template_name="login.html", context={'form': form})

def password_reset_request(request):
    if request.method == "POST":
        domain = request.headers['Host']
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            print("associated_users ", associated_users)
            # You can use more than one way like this for resetting the password.
            # ...filter(Q(email=data) | Q(username=data))
            # but with this you may need to change the password_reset form as well.

            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_subject.txt"
                    c = {
                        "email": user.email,
                        'domain': domain,
                        'site_name': 'Interface',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset_form.html",
                  context={"password_reset_form": password_reset_form})


