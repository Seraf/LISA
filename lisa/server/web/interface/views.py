from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required()
def dashboard(request):
    return render(request, 'dashboard.html', {
    })


def login(request):
    from django.contrib.auth import login
    from mongoengine.django.auth import User
    from mongoengine.queryset import DoesNotExist
    from django.contrib import messages
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST['username'])
            if user.check_password(request.POST['password']):
                user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                print login(request, user)
                request.session.set_expiry(60 * 60 * 1)  # 1 hour timeout
                return redirect('dashboard')
            else:
                messages.add_message(request,messages.ERROR, u"Incorrect login name or password !")
        except DoesNotExist:
            messages.add_message(request,messages.ERROR, u"Incorrect login name or password !")
        return render(request, 'login.html', {})
    else:
        return render(request, 'login.html', {})


def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')

@login_required()
def index(request):
    return render(request, 'index.html', {
    })