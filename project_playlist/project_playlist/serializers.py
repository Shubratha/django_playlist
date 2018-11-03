from rest_framework import serializers
from project_playlist.models import Playlist,Song
from django.contrib.auth.models import User

class SongSerializer(serializers.ModelSerializer):
    # playlist= serializers.StringRelatedField()
    # playlist = serializers.RelatedField(source='playlist.name', read_only=True)
    playlist = serializers.PrimaryKeyRelatedField(queryset=Playlist.objects.all())
    class Meta:
        model = Song
        fields = ('id','playlist','url','name')

class PlaylistSerializer(serializers.ModelSerializer):
    # songs = serializers.StringRelatedField(many=True)
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model= Playlist
        fields = ('id','user','name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
