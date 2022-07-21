from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile


def signup(request):
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
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password)
                user.save()

                user_login = auth.authenticate(username=username,
                                               password=password)
                auth.login(request, user_login)
                messages.success(request, "ثبت نام با موفقیت انجام شد.")

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model,
                                                     email=email)
                new_profile.save()
                print(new_profile)

                return redirect('profile')
        else:
            messages.info(request, "رمز عبور مشابه نمی باشد.")
            return redirect('signup')
    else:
        return render(request, 'registration/signup.html')


def login(request):
    if request.method == "POST":
        
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,
                                 password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('profile')
        else:
            messages.info("اطلاعات نامعتبر می باشد.")
            return redirect('login')
    else:
        return render(request, 'registration/login.html')


def log_out(request):
    auth.logout(request)
    return redirect('login')


def profile(request):
    user = request.user
    print(user.id)
    profile = Profile.objects.get(user_id=user.id)
    print(profile)
    return render(request, 'registration/profile.html', {'profile': profile})