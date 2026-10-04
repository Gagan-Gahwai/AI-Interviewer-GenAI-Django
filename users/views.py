from django.shortcuts import render
from django.http import JsonResponse
from .models import User
import json
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Create your views here.

@csrf_exempt
def register_user(request):
    if request.method== 'POST':

        data = json.loads(request.body)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'message': 'Username Already exists'
            }, status = 400)

        elif User.objects.filter(email=email).exists():
            return JsonResponse({
                'message' : 'Email already exits'
            }, status = 400)

        hashed_password = make_password(password)

        user = User.objects.create(
            username = username,
            email = email,
            password = hashed_password
        )

        return JsonResponse({
            'message' : 'User registered succesfully',
            'user' : {
                'id' : user.id,
                'username' : user.username,
                'email' : user.email
            }
        }, status = 201)

    return JsonResponse({
        'message' : "only post request allowed"
    }, status = 405)

@csrf_exempt
def login_user(request):

    if request.method == "POST":

        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                "message" : "Invalid username or password"
            }, status = 401)

        if not check_password(password, user.password):
            return JsonResponse({
                "message": 'Invalid username or password'
            }, status = 401)

        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            'message': "Login successful",
            'access' : str(refresh.access_token),
            'refresh': str(refresh)
        }, status = 200)

    return JsonResponse({
        "message": 'Only POST request allowed'
    }, status = 405)

@csrf_exempt
def get_current_user(request):

    if request.method != "GET":
        return JsonResponse({
            "message": "Only GET request allowed"
        }, status=405)

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JsonResponse({
            "message": "Authorization token required"
        }, status=401)

    try:
        token = auth_header.split(" ")[1]

        access_token = AccessToken(token)

        user_id = access_token["user_id"]

        user = User.objects.get(id=user_id)

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

    except Exception:
        return JsonResponse({
            "message": "Invalid or expired token"
        }, status=401)


@csrf_exempt
def logout_user(request):

    if request.method != "POST":
        return JsonResponse({
            "message" : "Only POST request allowed"
        }, status = 405)

    data = json.loads(request.body)

    refresh_token = data.get('refresh')

    if not refresh_token:
        return JsonResponse({
            "message" : "Refresh token is required"
        }, status = 400)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

        return JsonResponse({
            'message': "Logout succesful"
        }, status = 200)

    except Exception:
        return JsonResponse({
            'message': "Invalid refresh token"
        }, status= 400)