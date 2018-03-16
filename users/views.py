from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', context={'form': form})


@login_required # 登录状态验证
def account(request):
    return render(request, 'users/user_center_p2.html')

def user_center(request):
    return render(request, 'users/user_center_p1.html')


    

