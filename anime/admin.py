# In admin.py of the anime app
from django.contrib import admin
from .models import Anime

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'synopsis', 'genre', 'aired', 'episodes', 'members', 'popularity', 'ranked', 'score', 'img_url', 'link')
