from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView
from .forms import LoginForm, SignupForm
from .models import Profile


class SignUpView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignupForm

    def form_valid(self, form):
        request = self.request
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        password2 = form.cleaned_data['password2']
        email = form.cleaned_data['email']

        new_user = User.objects.create(username=username,
                                       email=email,
                                       password=password)
        new_user.set_password(password2)
        new_user.save()

        new_user_login = auth.authenticate(username=username,
                                           password=password)
        auth.login(request, new_user_login)
        messages.success(request, "ثبت نام با موفقیت انجام شد.")
        return redirect('profile')



# def signup(request):
#
#     if request.method == "POST":
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = request.POST['password2']
#
#         if username == "":
#             messages.info(request, "نام کاربری نمی تواند خالی باشد.")
#             return redirect('signup')
#
#         elif password == password2:
#             if User.objects.filter(email=email).exists():
#                 messages.info(request, "ایمیل قبلا ثبت شده است.")
#                 return redirect('signup')
#             elif User.objects.filter(username=username).exists():
#                 messages.info(request, "نام کاربری قبلا ثبت شده است.")
#                 return redirect('signup')
#             else:
#                 new_user = User.objects.create(username=username,
#                                                email=email,
#                                                password=password)
#                 new_user.set_password(password2)
#                 new_user.save()
#
#                 new_user_login = auth.authenticate(username=username,
#                                                    password=password)
#                 auth.login(request, new_user_login)
#                 messages.success(request, "ثبت نام با موفقیت انجام شد.")
#
#                 return redirect('profile')
#         else:
#             messages.info(request, "رمز عبور مشابه نمی باشد.")
#             return redirect('signup')
#     else:
#         return render(request, 'registration/signup.html')


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        request = self.request
        valuenext = request.POST.get('next')
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and valuenext == '':
            login(request, user)
            return redirect('profile')
        elif user is not None and valuenext != '':
            login(request, user)
            return redirect(valuenext)
        else:
            messages.info(request, "اطلاعات وارد شده نامعتبر می باشد.")
            return redirect('login')


class LogOutView(View):
    @method_decorator(login_required)
    def get(self, request):
        auth.logout(request)
        return redirect('login')


@login_required()
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        province = request.POST.get('province')
        city = request.POST.get('city')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code')

        profile.phone_number = phone_number
        profile.province = province
        profile.city = city
        profile.address = address
        profile.postal_code = postal_code
        profile.save()
    return render(request, 'registration/profile.html', {'profile': profile})
