from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User, auth
from .models import user_collection
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Profile, Post, Broadcast, LikePost, FollowersCount
from itertools import chain
import random


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))
    
    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))


    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list,'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        write_post = request.POST['write_post']

        if image is not None:
            new_post = Post.objects.create(user=user, image=image, write_post=write_post)
            new_post.save()
        if image is None:
            new_post = Post.objects.create(user=user, write_post=write_post)
            new_post.save()

        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_broadcast = Broadcast.objects.filter(user=pk)
    user_post_length = len(user_posts)
    user_broadcast_length = len(user_broadcast)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'user_broadcast' : user_broadcast,
        'user_broadcast_length' : user_broadcast_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def broadcast(request):

    user_profile = Profile.objects.get(user=request.user)
    user = request.user.username
    broadcast = request.POST['broadcast']

    if user_profile.role == 'company_hr':
        new_post = Broadcast.objects.create(user=user, broadcast=broadcast)
        new_post.save()
        return redirect('/')
    else:
        messages.info(request, 'Only company hr can broadcast')
        return redirect('/')

@login_required(login_url='signin')
def broadcast_panel(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    broadcast = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        broadcast_lists = Broadcast.objects.filter(user=usernames)
        broadcast.append(broadcast_lists)

    broadcast_list = list(chain(*broadcast))
    return render(request, 'broadcast.html',{'user_profile': user_profile, 'broadcasts':broadcast_list})
    

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')
    

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            user_profile.profileimg = image
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')

            user_profile.profileimg = image
            user_profile.save()
        
        return redirect('settings')

    return render(request, 'profile_setting.html', {'user_profile' : user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['confirm_password']
        role = request.POST['role']

        if password == password2:
            if user_collection.find_one({"email": email}):
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif user_collection.find_one({"username": username}):
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                record = {
                        "username" : username,
                        "email" : email,
                        "password" : password,
                        "role" : role

                }
                user_collection.insert_one(record)

                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id,role=role)
                new_profile.save()
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = user_collection.find_one({"username": username})

        if user is not None:
            pass_check = user["password"]
            if pass_check == password:
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
            else:
                messages.info(request, 'Invalid password')
                return redirect('signin')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url= 'signin')
def logout(request):
    auth.logout(request)
    return redirect(signin)

@login_required(login_url= 'signin')
def chat(request):
    users = FollowersCount.objects.filter(follower=request.user.username)
    return render(request, 'chat_index.html', context={'users': users})


@login_required(login_url= 'signin')
def chat_page(request, pk):
    user_obj = User.objects.get(username=pk)
    users = FollowersCount.objects.filter(follower=request.user.username)
    return render(request, 'chat.html', context={'users' : users,'user':user_obj})
