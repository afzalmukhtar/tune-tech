# Generated by Django 2.2.5 on 2021-09-03 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song', models.CharField(default='Unknown', max_length=100)),
                ('artist', models.CharField(default='Unknown', max_length=100)),
                ('album', models.CharField(default='Unknown', max_length=100)),
                ('duration', models.IntegerField(default=0)),
                ('lyrics_mood', models.CharField(choices=[('angry', 'angry'), ('happy', 'happy'), ('relaxed', 'relaxed'), ('sad', 'sad'), ('neutral', 'neutral')], default=None, max_length=10)),
                ('audio_mood', models.CharField(choices=[('calm', 'calm'), ('energetic', 'energetic'), ('happy', 'happy'), ('sad', 'sad')], default=None, max_length=10)),
                ('audio_file', models.FileField(blank=True, default=None, upload_to='songs')),
            ],
        ),
    ]
