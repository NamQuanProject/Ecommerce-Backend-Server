from django.shortcuts import render
import json 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages, auth
from .models import CustomUser
from .models import Profile, Friend
from django.http import HttpResponse, JsonResponse
from django.core import serializers

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        full_name = data.get('full_name')
        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')
        password2 = data.get('password2')


        if password == password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "This username is already taken")
                return JsonResponse({"status": 'That username is taken'}, status=400)

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "This email is already taken")
                return JsonResponse({"status": 'That email is taken'}, status=400)

            profile = Profile.objects.create(full_name=full_name)
            user = CustomUser.objects.create_user(username=username, password=password, email=email, phone_number=phone_number, profile=profile)
            user.save()
            auth.login(request, user, 'users.backends.EmailBackend')


            return JsonResponse({"status": "User registered successfully"})
        else:
            return JsonResponse({"status": 'Passwords do not match'}, status=400)
    else:
        return HttpResponse("Register")



@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        user = auth.authenticate(request = request, email = email , password = password)

        if user is not None:
            print("User is not none")
            auth.login(request, user = user ) 
            messages.success(request, 'You are now logged in')
            return JsonResponse({"status" : "You are now login"}, status = 200)
        else:
            print("There is no user")
            messages.error(request, "no user")
            return JsonResponse(
                {"status": "Invalid credentials"},
                status=403
            )
    else:
        return HttpResponse("Login")


@csrf_exempt
def logout(request):
    # if not request.user.is_authenticated:
    #     return JsonResponse(
    #         {"status": "Unauthenticated"},
    #         status=400
    #     )
    if request.method=="POST":
        auth.logout(request)
        messages.success(request, "You are now logged out")
        return JsonResponse(
            {"status": "You are now logged out"},
            status=200
        )
    else: return HttpResponse("Logout")



def get_all_users(request):
    if request.method == "GET":
        data = []
        users = CustomUser.objects.all()
        for user in users:
            
            profile_data = {
                "id" : user.profile.id,
                "username" : user.username,
                "email" : user.email,
                "password" : user.password,
                "full_name": user.profile.full_name,
                "bio": user.profile.bio,
                # Add other profile fields as needed
            }
            data.append(profile_data)

        return JsonResponse(data, safe=False, status=202)



@csrf_exempt
def profile(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "Unauthenticated"},
            status=400
        )
    if request.method=="PUT":
        data = json.loads(request.body)
        profile = request.user.profile
        profile.full_name, profile.bio = data.get('full_name'), data.get('bio')
        profile.save()
        return JsonResponse({"status": "Updated profile"}, status=200)
    elif request.method=="GET":
        profile = request.user.profile
        return JsonResponse({
            "full_name": profile.full_name,
            "bio": profile.bio,
        }, status=200)



def get_user(request, user_id):
    
    if request.method=="GET":
        try:
            user = CustomUser.objects.get(id=user_id)
            profile = user.profile
            #messages.success(f"Found user {user_id}")
            return JsonResponse({
                "full_name": profile.full_name,
                "bio": profile.bio,
            }, status=200)
        except CustomUser.DoesNotExist:
            #messages.error(f"User {user_id} does not exist")
            return JsonResponse({"status": f"User {user_id} does not exist"}, status=404)

def friends(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "Unauthenticated"},
            status=400
        )
    if request.method=="GET":
        user_friends = Friend.objects.filter(user_from=request.user).values_list('user_to', flat=True)
       
        users = []
        for user_id in user_friends:
            user = CustomUser.objects.get(id = user_id)
            users.append({"username" : user.username, "id": user_id})
    
        print(users)

        return JsonResponse(users, status=200, safe = False)


@csrf_exempt
def make_friend(request, user_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "Unauthenticated"},
            status=400
    )
    if request.method == "GET":
        user = CustomUser.objects.get(id=user_id)
        user_friends = Friend.objects.filter(user_from=user).values_list('user_to', flat=True)

        friends_list = list(user_friends)
        response_data = {"user_friends": friends_list}

        return JsonResponse(response_data, status=200)
    
    elif request.method=="POST":
        
        user1 = CustomUser.objects.get(id=request.user.id)
        user2 = CustomUser.objects.get(id=user_id)
        if (user1 == user2):
            return JsonResponse({"status" : "Same person"}, status = 402)
        
        friendship = Friend(user_from = user1 , user_to = user2)
        bi_friendship = Friend(user_from = user2, user_to = user1)
        if (Friend.objects.filter(user_from = user1 , user_to = user2).exists()):
            return JsonResponse({"status" : "You have already been friends" }, status = 202)
        friendship.save()
        bi_friendship.save()
        return JsonResponse({"status" : "They are friends now" }, status = 202)

        
    