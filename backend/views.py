from os import stat, remove
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import status

from .models import Song, Image, User
from .serializers import SongSerializer, UserSerializer
from django.contrib import messages




# Imports and Globals
from django.conf import settings
ModelDriver = settings.MODELDRIVER
SONG_DETAILS = dict()
LOGGED_IN = False

# Create your views here.


@api_view(['GET'])
def apiOverview(request):
    """To Get a view of all API Calls Allowed"""
    api_urls = {
        'Add Song Info' : 'add_song_info',
        'Upload Song' : 'upload_song',
        'Listen Now' : 'generate_playlist',
        'Browse' : 'display_songs',
    }
    return Response(api_urls)

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def dashboard(request, username):
    """To Load the Dashboard"""
    user = User.objects.get(username=username)
    if LOGGED_IN:
        return Response(data={"user_name" : user.username, "user_image" : user.image}, status=status.HTTP_200_OK, template_name='dashboard.html')
    return Response(data={"message" : "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED, template_name='login.html')

def index(request):
    return render(request, 'login.html')

@api_view(['POST'])
def add_song_info(request):
    global SONG_DETAILS
    data = request.data
    song_name, artist_name = data['song'], data['artist']
    SONG_DETAILS = ModelDriver.get_song_data(song_name, artist_name)
    # print(SONG_DETAILS)
    return Response(data=SONG_DETAILS, status=status.HTTP_200_OK)

class Upload_Song(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        data = request.data
        data.update(SONG_DETAILS)
        SONG_DETAILS.clear()
        serializer = SongSerializer(data=data)
        # print("SERIALIZER DATA Initial: ", serializer.initial_data)
        
        if serializer.is_valid():
            serializer.save()
            # print("SERIALIZER DATA: ", serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def display_songs(request):
    song_info = Song.objects.all()
    serializer = SongSerializer(song_info, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def generate_playlist(request):
    
    if request.method == 'GET':
        image_url = '.' + Image.objects.order_by('-time_of_image')[0].image.url
        emotions = ModelDriver.get_face_emotion(image_url)
    if request.method == 'POST':
        emotions = [request.data['mood'], 'neutral']

    song_info = Song.objects.all()
    serializer = SongSerializer(song_info, many=True)
    recommendations = ModelDriver.recommend_song(song_list=serializer.data, mood_list=emotions)
    song_list = [i[1] for i in recommendations]
    artist_list = [i[2] for i in recommendations]
    recommendations = []
    for song, artist in zip(song_list, artist_list):
        recommendations.append(Song.objects.get(song=song, artist=artist))
    
    serializer = SongSerializer(recommendations, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def login_check(request):
    global LOGGED_IN
    try:
        user = User.objects.get(email=request.data['email'], password=request.data['password'])
        if user:
            LOGGED_IN = True
            return Response(data={"message": "Sign In Successful", "username" : user.username}, status=status.HTTP_202_ACCEPTED)
    except Exception:
        return Response(data={"message": 'Check Username/Password'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(data={"message": 'Check Username/Password'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def signup_check(request):
    user = User()
    print(request.data)
    user.email, user.username, user.password = request.data['email'], request.data['username'], request.data['password']
    if User.objects.filter(username=user.username).exists() or User.objects.filter(email=user.email).exists():
        return Response(data="Username/Email already exists", status=status.HTTP_409_CONFLICT)
    else:
        user.save()
        return Response(data="User Creation Successful", status=status.HTTP_201_CREATED)

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def logout(requests):
    global LOGGED_IN
    LOGGED_IN = False
    return Response(data={"message" : "Logged Out"}, status=status.HTTP_308_PERMANENT_REDIRECT, template_name='login.html')


class UserAvatarUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, username, format=None):
        # print("Initial Print: ", request.data, username)
        data = request.data
        # print(data['image'])
        user = User.objects.get(username=username)
        old_file = user.image.path
        user.image = data['image']
        
        if user:
            user.save()
            if "default_avatar" not in old_file:
                remove(old_file)
            return Response({"message" : "Successfully Update", "image" : user.image.url}, status=status.HTTP_200_OK)
        else:
            return Response({"message" : "Error Occured"}, status=status.HTTP_400_BAD_REQUEST)

# def signup(requests):
#     users = User()
#     users.usn, users.email, users.passwd = requests.POST['usn'], requests.POST['email'], requests.POST['passwd']
#     if User.objects.filter(usn=users.usn).exists() or User.objects.filter(email=users.email).exists():
#         messages.info(requests, 'Username Taken', extra_tags='signup')
#     else:
#         users.save()
#     return redirect('/')

# def edit(requests, usn, admin):
#     user_details = User.objects.get(usn=usn)
#     admin_details = User.objects.get(usn=admin)
#     return render(requests, 'edit.html', {'user' : user_details, 'admin' : admin_details})

# def update(requests, usn, admin):
#     admin = User.objects.get(usn=admin)
#     result = User.objects.get(usn=usn)
#     form = UpdateForm(requests.POST, instance=result)
#     if form.is_valid():
#         form.save()
#         messages.success(requests, "Record is Updated", extra_tags='update')
#     result = User.objects.all()
#     return render(requests, 'display1.html', {'users' : result, 'admin' : admin})

# def delete(requests, usn, admin):
#     admin = User.objects.get(usn=admin)
#     result = User.objects.get(usn=usn)
#     result.delete()
#     messages.success(requests, "Record Deleted", extra_tags='delete')
#     result = User.objects.all()
#     if not result.__len__():
#         return redirect("/")
#     return render(requests, 'display1.html', {'users' : result, 'admin' : admin})

