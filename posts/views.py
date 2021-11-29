from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Post
from django.views.decorators.clickjacking import xframe_options_exempt


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@xframe_options_exempt
def home(request):
    all_posts = Post.objects.all()
    return render(request=request, template_name="home.html", context = {"user":request.user, 'posts': all_posts})