from rest_framework import serializers
from .models import Song, User

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["song", "artist", "album", "duration", "lyrics_mood", "audio_mood", "album_art", "audio_file"]




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "image"]