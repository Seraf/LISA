from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext,Template,Context,loader

def login(request):
    from django.contrib.auth import login
    from mongoengine.django.auth import User
    from mongoengine.queryset import DoesNotExist
    from django.contrib import messages
    try:
        user = User.objects.get(username=request.POST['username'])
        if user.check_password(request.POST['password']):
            user.backend = 'mongoengine.django.auth.MongoEngineBackend'
            print login(request, user)
            request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
            print "return"
            return redirect('index')
        else:
            messages.add_message(request,messages.ERROR,u"Incorrect login name or password !")
    except DoesNotExist:
        messages.add_message(request,messages.ERROR,u"Incorrect login name or password !")
    return render(request, 'login.html', {})

def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')


def index(request):
    return render(request, 'index.html', {
    })