from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from cart.models import Cart


def signup(request):
    new_cart = None
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "ایمیل قبلا ثبت شده است.")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "نام کاربری قبلا ثبت شده است.")
                return redirect('signup')
            else:
                new_user = User.objects.create(username=username,
                                               email=email,
                                               password=password)
                new_user.set_password(password2)
                new_user.save()

                new_user_login = auth.authenticate(username=username,
                                                   password=password)
                auth.login(request, new_user_login)
                messages.success(request, "ثبت نام با موفقیت انجام شد.")

                # user_profile = User.objects.get(username=username)
                # # new_profile = Profile.objects.create(user=user_profile,
                # #                                      email=email)
                # # new_profile.save()
                #
                # cart_profile = Profile.objects.get(user=user_profile)
                # new_cart = Cart.objects.create(username=cart_profile)
                return redirect('profile')
        else:
            messages.info(request, "رمز عبور مشابه نمی باشد.")
            return redirect('signup')
    else:
        return render(request, 'registration/signup.html')


def login(request):
    if request.method == "POST":
        valuenext = request.POST.get('next')
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,
                                 password=password)

        if user is not None and valuenext == '':
            auth.login(request, user)
            return redirect('profile')
        elif user is not None and valuenext != '':
            auth.login(request, user)
            return redirect(valuenext)
        else:
            messages.info(request, "اطلاعات وارد شده نامعتبر می باشد.")
            return redirect('login')
    else:
        return render(request, 'registration/login.html')


@login_required()
def log_out(request):
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
