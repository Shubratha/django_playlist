from django.shortcuts import render, redirect
from django.contrib.auth  import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Playlist,Song
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'project_playlist/signup.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            return HttpResponse(form.errors)
        form.save()
        user= User.objects.get(username= form.cleaned_data.get('username'))
        login(request, user)
        return render(request, 'project_playlist/signup.html', {'form': form})
    else:
        return HttpResponse("Unsupported method")

def login_view(request):
    if request.method == 'GET':
        if not request.user.is_anonymous:
            return redirect('/playlists')
        else:
            form = AuthenticationForm()
            return render(request, 'project_playlist/login.html', {'form': form})
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/playlists')
        else:
            return render(request, 'project_playlist/login.html', {'form': form})


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/login/")


def get_playlist(request,playlist_id):
    #import pdb; pdb.set_trace()
    if request.method == 'GET':
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return HttpResponse("Playlist not available",content_type="text/html")
        playlist = Playlist.objects.get(id=playlist_id)
        if playlist.user.id == request.user.id:
            context = {'playlist': playlist, 'is_owner':True}
        else:
            context = {'playlist':playlist, 'is_owner':False}
        print(request.user.id)
        print(playlist.user.id)
        songs = Song.objects.all()
        return render(request, 'project_playlist/playlist.html',context)
    elif request.method == 'POST':
        playlist = Playlist.objects.get(id = playlist_id)
        if playlist.user.id == request.user.id:
            url=request.POST.get('url')
            name=request.POST.get('name')
            if url and name:
                song = Song()
                song.playlist=playlist
                song.url=url
                song.name=name
                song.save()
                return render(request,'project_playlist/playlist.html',{'playlist':playlist})
            else:
                return HttpResponse("Enter song name and valid url")
        else:
            return render(request,'project_playlist/playlist.html',{'playlist':playlist})




def get_all_playlist(request):
    if request.user.is_anonymous:
        return redirect('/login/')
    if request.method == 'GET':
        playlists = Playlist.objects.filter(user=request.user)
        context = {'playlists':playlists} 
        print(request.user)
        return render(request, 'project_playlist/playlists.html',context)
    elif request.method == 'POST':
        title= request.POST.get('title')
        if title:
            Playlist.objects.create(name=title, user=request.user)
            return redirect('/playlists')
        else:
            return HttpResponse("Enter playlist name")



