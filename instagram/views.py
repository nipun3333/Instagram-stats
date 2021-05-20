from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from instaloader import Instaloader, Profile
import pandas as pd
from django.core.paginator import Paginator, EmptyPage
import os
import instaloader
from .import models

class MyRateController(instaloader.RateController):
    def count_per_sliding_window(self, query_type):
        return 302


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            return redirect('log_in')
        except:
            print(123)
            messages.add_message(request, messages.ERROR, 'not able to sign up')
            return render(request, 'register.html')
    
    return render(request, 'register.html')

def user_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user_obj = authenticate(username=username, password=password)
            login(request, user_obj)
            request.session['username'] = username
            return redirect('home')
        except:
            messages.add_message(request, messages.ERROR, 'Not able to log in')
            return render(request, 'login.html')
    
    return render(request, 'login.html')


def user_logout(request):
    try:
        logout(request)
        print(123)
    except:
        messages.add_message(request, messages.ERROR, 'can not logout')
    
    return redirect('home')

@login_required
def data(request):
    if request.user.is_authenticated:
        user_obj = User.objects.get(id = request.user.id)
        
            
    target_profile = 'bankingpledge'

    
    loader = Instaloader(sleep=False, rate_controller=lambda ctx: MyRateController(ctx))

    profile = Profile.from_username(loader.context, target_profile)

    followers = profile.followers
    followings = profile.followees
    full_name = profile.full_name
    biography = profile.biography

    print(followers, followings, full_name, biography)

    # loader.interactive_login('nipun3333')
    # loader.load_session_to_file('nipun3333')
    
    
    pre = os.path.dirname(os.path.realpath(__file__))
    fname = 'Instagram_URL.xlsx'
    path = os.path.join(pre, fname)
    dp = pd.read_excel(path)


    usernames = []
    for i in dp['Instagram URL']:
        usernames.append(i.split('/')[-2])
    

    users = []
    f = open('data.txt', 'r', encoding="utf-8")
    lines = f.readlines()
    i = 0
    fl_mn = request.GET.get('followers-min', 0)
    fl_mx = request.GET.get('followers-max', 1000000000)
    # print(lines, len(lines))
    while i<len(lines):
        if lines[i]=='>><<\n':
            i+=1
            if i==len(lines):
                break
            username, followers, followings, full_name = lines[i].split(',')
            followers, followings = int (followers), int(followings)
            i+=1
        bio = ""
        
        while lines[i]!='>><<\n':
            bio+=(lines[i]+'\n')
            # print(i, lines[i])
            i+=1
        if followers>=int(fl_mn) and followers<=int(fl_mx):
            users.append({"username":username, "followers":followers, "followings":followings, "full_name":full_name, "bio":bio})
        
        # print(1234, i, 1234, len(lines))
        # print(users)


    f.close()
    # print(users)
    # i=1
    # f = open('data.txt', "a", encoding="utf-8")
    # f.write(">><<")
    # for username in usernames:
    #     profile = Profile.from_username(loader.context, username)
    #     followers = profile.followers
    #     followings = profile.followees
    #     full_name = profile.full_name
    #     bio = profile.biography

    #     f.write(username+','+str(followers)+','+str(followings)+','+full_name+'\n')
    #     f.write(bio)
    #     f.write("\n>><<\n")
    #     # print(users)
    #     print(i, username)
    #     i+=1
    # f.close()
    
    
    p = Paginator(users, 10)

    page_num = request.GET.get('page', 1)

    try:
        users = p.page(page_num)
    except EmptyPage:
        users = p.page(1)

    return render(request, 'data.html', {"users":users})






# window.location.href += ("follower-min="$( "#amount" ).val($("#slider-range").slider("values", 0))+"&"+"follower-max="$( "#amount" ).val($("#slider-range").slider("values", 1)));