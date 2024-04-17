from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .forms import RegisterForm

# request를 받아 response를 처리하는 함수


def index(request):
    return render(request, 'user/profile.html')
    # print(dir(request))
    #
    request_attrs = dir(request)
    for attr in request_attrs:
        print(attr, getattr(request, attr))
        print('-'*10)
    return HttpResponse(html)

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request,user)
            return redirect(reverse('user:index'))
    return render(request, 'user/register.html', {'form':form})
# Create your views here.
