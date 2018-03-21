from django.shortcuts import render, redirect, get_object_or_404
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


def account(request):
    if not request.user.is_authenticated:
        return redirect('/%s?next=%s' % (settings.LOGIN_URL, request.path))

    return render(request, 'users/user_center_p2.html')


# @login_required
def user_center(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    context = {
        'username': user.username,
    }

    return render(request, 'users/user_center_p1.html', context)


def password_reset_X(request):
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
            user_id = user.id
            user_name = user.username

            def GenPassword(length=8, chars=string.ascii_letters + string.digits):
                return ''.join([choice(chars) for i in range(length)])
            reset_passwd = GenPassword(8)

            User.objects.filter(email=email).delete()
            User.objects.create_user(id=user_id, username=user_name, password=reset_passwd, email=email)

            send_mail(
                subject="这是新的密码,请使用新的密码登录",
                message=reset_passwd,
                from_email='m15211180180@163.com',
                recipient_list=[email,],
                fail_silently=False,
            )

            return render(request, 'registration/password_reset_done.html')

    # print(email)


    return render(request, 'registration/password_reset_form.html')


# class PasswordContextMixin:
#     extra_context = None
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'title': self.title,
#             **(self.extra_context or {})
#         })
#         return context
#
#
# class PasswordResetView(PasswordContextMixin, FormView):
#     email_template_name = 'registration/password_reset_email.html'
#     extra_email_context = None
#     form_class = PasswordResetForm
#     from_email = None
#     html_email_template_name = None
#     subject_template_name = 'registration/password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')
#     template_name = 'registration/password_reset_form.html'
#     title = _('Password reset')
#     token_generator = default_token_generator
#
#     @method_decorator(csrf_protect)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     def form_valid(self, form):
#         opts = {
#             'use_https': self.request.is_secure(),
#             'token_generator': self.token_generator,
#             'from_email': self.from_email,
#             'email_template_name': self.email_template_name,
#             'subject_template_name': self.subject_template_name,
#             'request': self.request,
#             'html_email_template_name': self.html_email_template_name,
#             'extra_email_context': self.extra_email_context,
#         }
#
#         # print(self.form_class.email)
#
#         form.save(**opts)
#         return super().form_valid(form)
