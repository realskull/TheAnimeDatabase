from django.urls import path
#from anime.views import index, anime, fetch_genres, genre, fetch_genre, search, fetch_results  # Import the index view from your app
from anime.views import *
urlpatterns = [
    path('', index, name='index'),  # Map the empty string to the index view
    # Add other URL patterns as needed
    path('/about', about, name='about'),
    path('/anime', anime, name='anime'),
    path('/genre', genre, name='genre'),
    path('/search', search, name='search'),
    path('fetch-genres/', fetch_genres, name='fetch_genres'),
    path('fetch_genre/', fetch_genre, name='fetch_genre'),
    path('fetch_results/', fetch_results, name='fetch_results')
    
]
