from django.http import JsonResponse
from django.shortcuts import redirect, render
import requests
from .models import Account
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_page(request):
    if request.POST:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect(created)
        else:
            return redirect(login_page)    

    return render(request, "login.html")

def signup_page(request):
    if request.POST:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        username = request.POST.get('username', '')
        user = Account.objects.filter(Q(email=email), Q(username=username))
        if user:
            return redirect(signup_page)
        else:
            user = Account.objects.create_user(
                email=email,
                username=username,
                password=password,
            )    
            login(request, user)
            return redirect('/account/created')
    return render(request, "signup.html")
    

@login_required(login_url='/account/login')
def created(request):
    return render(request, "created.html")    


def verify_telegram(request):
    user = request.user.username
    url = 'https://api.telegram.org/bot5980251499:AAG2pFjNpT7v-62Uk7w9Jnt92QGppxXX8p0/getUpdates'
    resp = requests.get(url).json()
    result = resp['result']
    users = []
    for i in result:
        if i.get('my_chat_member'):
            username = i['my_chat_member']['chat']['username']
            if username == user:
                if i["my_chat_member"]['new_chat_member']["status"] == "member":
                    if username not in users:
                        users.append(username)
                else:
                    while username in users:
                        users.remove(username)   
            
    if request.user.username in users:
        msg = "success"    
    else:
        msg = "failed"        
    return JsonResponse({"message": msg, "username": request.user.username})