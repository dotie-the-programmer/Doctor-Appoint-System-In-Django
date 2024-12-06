from django.shortcuts import render, redirect, HttpResponse
from dasapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dasapp.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


def BASE(request):
    return render(request, 'base.html')


def LOGIN(request):
    return render(request, 'login.html')


def doLogout(request):
    logout(request)
    return redirect('login')


def doLogin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'),
                                         password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('admin_home')
            elif user_type == '2':
                return redirect('doctor_home')
            elif user_type == '3':
                return HttpResponse("This is User panel")
        else:
            messages.error(request, 'Email or Password is not valid')
            return redirect('login')
    else:
        messages.error(request, 'Email or Password is not valid')
        return redirect('login')


# Ensure @login_required is used with the @ symbol
@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')

        # Check if profile_pic is not None or blank before saving
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            if profile_pic:
                customuser.profile_pic = profile_pic
            customuser.save()

            messages.success(request, "Your profile has been updated successfully")
            return redirect('profile')

        except Exception as e:
            messages.error(request, f"Your profile updation has failed: {str(e)}")

    return render(request, 'profile.html')


@login_required(login_url='/')
def CHANGE_PASSWORD(request):
    context = {}
    ch = User.objects.filter(id=request.user.id)
    if len(ch) > 0:
        data = User.objects.get(id=request.user.id)
        context["data"] = data

    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id=request.user.id)
        un = user.username

        # Check current password
        check = user.check_password(current)
        if check:
            user.set_password(new_pas)
            user.save()
            messages.success(request, 'Password changed successfully!')
            user = User.objects.get(username=un)
            login(request, user)
        else:
            messages.error(request, 'Current Password is incorrect!')
            return redirect("change_password")

    return render(request, 'change-password.html', context)
