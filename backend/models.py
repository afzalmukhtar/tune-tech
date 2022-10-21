from django.db import models

# Create your models here.

class Song(models.Model):
    song = models.CharField(max_length=100, default='Unknown')
    artist = models.CharField(max_length=100, default='Unknown')
    album = models.CharField(max_length=100, default='Unknown')
    duration = models.IntegerField(default=0)
    
    LyricsMoodChoices = [('angry', 'angry'), ('happy', 'happy'), ('relaxed', 'relaxed'), ('sad', 'sad'), ('neutral', 'neutral')]
    lyrics_mood = models.CharField(max_length=10, choices=LyricsMoodChoices, default=None)
    
    AudioMoodChoices = [('calm', 'calm'), ('energetic', 'energetic'), ('happy', 'happy'), ('sad', 'sad')]
    audio_mood = models.CharField(max_length=10, choices=AudioMoodChoices, default=None)

    audio_file = models.FileField(default=None, upload_to='songs', blank=True)

    album_art = models.CharField(max_length=100, default='static/album_art/default.png')

    def __str__(self) -> str:
        return self.song


class Image(models.Model):
    image = models.ImageField(upload_to='images', null=False, blank=True)
    time_of_image = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.time_of_image)

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    image = models.ImageField(upload_to='avatar', default='avatar/default_avatar.png', null=False, blank=True)

    def __str__(self) -> str:
        return self.username
