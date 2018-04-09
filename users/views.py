from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
# from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from .forms import PasswordResetForm
from django.core.mail import send_mail
from random import choice
import string
from movies.models import Comment

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

# @login_required
def account(request):
    if not request.user.is_authenticated:
        return redirect('/%s?next=%s' % (settings.LOGIN_URL, request.path))

    return render(request, 'users/user_center_p2.html')


def user_center(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # 确保登录后的用户 A 查看用户 B 的个人中心时，看不到账户管理的选项
    logged_in = False
    if request.user.is_authenticated and request.user.id == user.id:
        logged_in = True
    print(logged_in)

    comment_list = Comment.objects.filter(user_id=user.id)
    movie_list = [c.movie_id for c in comment_list]

    context = {
        'username': user.username,
        'movie_list': movie_list,
        'logged_in': logged_in,
    }

    return render(request, 'users/user_center_p1.html', context)


def password_reset_x(request):
    email = request.POST.get('email')

    print(email)

    if email == None:
        return render(request, 'registration/password_reset_form.html')
    else:
        try:
            user = User.objects.get(email=email)
        except:
            print('用户不存在')
            user_not_exist = 1
            return render(request, 'registration/password_reset_form.html', {'user_not_exist': user_not_exist})
        else:
            print('邮箱可找到')
            # user_id = user.id
            # user_name = user.username

            def GenPassword(length=8, chars=string.ascii_letters + string.digits):
                return ''.join([choice(chars) for i in range(length)])
            reset_passwd = GenPassword(8)

            # 设置新密码
            user.set_password(reset_passwd)
            user.save()
            # User.objects.filter(email=email).delete()
            # User.objects.create_user(id=user_id, username=user_name, password=reset_passwd, email=email)

            send_mail(
                subject="这是新的密码,请使用新的密码登录",
                message=reset_passwd,
                from_email='m15211180180@163.com',
                recipient_list=[email,],
                fail_silently=False,
            )

            return render(request, 'registration/password_reset_done.html')



def delete_account(request):
    if not request.user.is_authenticated:
        return redirect('/%s?next=%s' % (settings.LOGIN_URL, request.path))

    # 删除账号
    request.user.delete()

    return HttpResponseRedirect(reverse('movies:index'))





