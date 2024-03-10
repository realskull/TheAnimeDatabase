from django.urls import path
#from anime.views import index, anime, fetch_genres, genre, fetch_genre, search
from anime.views import *

urlpatterns = [
    path('', index, name='index'),
    path('about', about, name='about'),
    path('anime', anime, name='anime'),
    path('genre', genre, name='genre'),
    path('search', search, name='search'),
    path('fetch-genres/', fetch_genres, name='fetch_genres'),
    path('fetch_genre/', fetch_genre, name='fetch_genre'),
    path('fetch_results/', fetch_results, name='fetch_results')
    # Add other URL patterns as needed
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
