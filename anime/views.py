from django.shortcuts import render
from .models import Anime
from django.db.models import F, Count, Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.cache import cache

unique_genres = set()

def unique_genres_cache():
    global unique_genres
    if len(unique_genres) == 0:
        # Fetch unique genres if not already fetched
        genres = Anime.objects.values_list('genre', flat=True).distinct()  
        genres_list = []
        for genre_set in genres:
            genres_list.extend(genre_set.split(', '))
        unique_genres = sorted(set(genres_list))
        unique_genres = [genre.strip("'[]") for genre in unique_genres if genre]
        unique_genres = [genre.strip() for genre in unique_genres if genre]
        unique_genres.sort()
        unique_genres = list(set(unique_genres))
        unique_genres.sort()
    
    return unique_genres


def get_star_rating_html(score):
        # Calculate the number of filled stars (out of 5)
        filled_stars = int(score / 2)
        # Calculate the number of half-filled stars
        half_star = score % 2

        # Generate HTML for filled stars
        filled_html = '<span class="fa fa-star checked"></span>' * filled_stars

        # Generate HTML for half-filled star if applicable
        half_html = '<span class="fa fa-star-half-empty"></span>' if half_star else ''

        # Generate HTML for empty stars
        empty_stars_count = 5 - filled_stars - int(bool(half_star))
        empty_html = '<span class="fa fa-star-o"></span>' * empty_stars_count

    

        return filled_html + half_html + empty_html


def anime(request):
    uid = request.GET.get('uid', None)

    if uid is None:
        # Handle the case when uid is not provided in the query parameters
        # For example, you can return an error message or redirect to another page
        return render(request, 'error.html', {'message': 'UID is not provided in the query parameters'})
    
    
    try:
        # Assuming Anime model has fields like title, synopsis, genre, etc.
        anime = Anime.objects.get(uid=uid)  # Fetch the anime object from the database based on the uid
    except Anime.DoesNotExist:
        # Handle the case when no anime with the provided uid is found
        # For example, you can return an error message or redirect to another page
        return render(request, 'error.html', {'message': 'Anime with the provided UID does not exist'})
    
    anime.star_html = get_star_rating_html(anime.score)

    # Additional context data (if needed)
    context = {
        'anime': anime,
        'genres' : unique_genres_cache()
        # You can include more context data here if needed
    }
    
    

    # Pass the anime object and additional context to the template for rendering
    return render(request, 'anime.html', context)

def index(request):
    top_anime = Anime.objects.order_by('-score')[:10]  # Retrieve top 10 anime by score
    worst_anime = Anime.objects.exclude(score=0.0).order_by('score')[:10]
    
    for x in top_anime:
        x.star_html = get_star_rating_html(x.score)
    
        
    for x in worst_anime:
        x.star_html = get_star_rating_html(x.score)

    # Pass data to the template
    context = {
        'top_anime': top_anime,
        'worst_anime': worst_anime,
        'genres' : unique_genres_cache()
    }

    # Render the index.html template with the context data
    return render(request, 'index.html', context)

def fetch_genres(request):
    unique_genres_cache()
    
    # Get the page number from the request or default to the first page
    page_number = request.GET.get('page', 1)
    
    # Calculate start and end indexes for genres based on the page number
    start_index = (int(page_number) - 1) * 3
    end_index = start_index + 3
    
    # Slice unique genres to get genres for the current page
    current_genres = unique_genres[start_index:end_index]
    
    anime_by_genre = {}
    for genre in current_genres:
        anime_list = Anime.objects.filter(genre__contains=genre).order_by('-score')[:10]
        paginator = Paginator(anime_list, per_page=10)
        page_anime = paginator.get_page(1)  # Always get the first page for each genre
        serialized_anime = [{'title': anime.title, 'score': anime.score, 'img_url': anime.img_url, 'uid': anime.uid, 'star_html': get_star_rating_html(anime.score)} for anime in page_anime]
        anime_by_genre[genre] = serialized_anime
        

    if len(anime_by_genre) == 0:
        message = 'end'
    else:
        message = 'ok'
    
    
    # Pass the fetched anime by genre back as JSON response
    return JsonResponse({'anime_by_genre': anime_by_genre, 'message': message})

def genre(request):
    # Get the genre from the GET request
    genre = request.GET.get('genre', None)
    
    # Check if the genre is provided in the request
    if not genre:
        return render(request, 'error.html', {'error_message': 'Genre parameter is missing in the request'})
    
    # Fetch top 20 anime of the specified genre
    anime_list = Anime.objects.filter(genre__contains=genre).order_by('-score')[:20]
    genre_count = Anime.objects.filter(genre__contains=genre).count()
    
    # Add star_html attribute to each anime object
    for anime in anime_list:
        anime.star_html = get_star_rating_html(anime.score)  # Assuming you have a function for star rating
    
    # Pass data to the template
    context = {
        'anime_list': anime_list,
        'genre': genre,
        'genres' : unique_genres_cache(),
        'genre_count' : genre_count
    }
    
    # Render the genre.html template with the context data
    return render(request, 'genre.html', context)


def fetch_genre(request):
    # Get the page number from the request or default to the first page
    page_number = int(request.GET.get('page', 1))
    
    # Get the genre from the request.
    genre = request.GET.get('genre')
    
    if not genre:
        return JsonResponse({'error': 'Genre parameter is missing in the request'}, status=400)
    
    # Calculate start and end indexes for anime based on the page number
    per_page = 20  # Number of anime per genre page
    offset = 0  
    start_index = (page_number - 1) * per_page + offset
    end_index = start_index + per_page
    
    # Fetch anime for the specified genre
    anime_list = Anime.objects.filter(genre__contains=genre).order_by('-score')[start_index:end_index]
    
    # Serialize the anime objects
    serialized_anime = [{
        'title': anime.title,
        'score': anime.score,
        'img_url': anime.img_url,
        'uid': anime.uid,
        'star_html': get_star_rating_html(anime.score)
        # Add 'star_html' field here if needed
    } for anime in anime_list]
    
    # Pass the fetched anime by genre back as JSON response
    return JsonResponse({'anime_by_genre': serialized_anime, 'message': 'ok'})

def search(request):
    # Get the search query and genres from the GET request
    search_query = request.GET.get('query', None)
    search_genres = request.GET.get('genres')

    # Check if the search query is provided in the request. If not provided, all anime
    if not search_query:
        anime_list = Anime.objects.all()
        search_query = "everything"
    else: 
        anime_list = Anime.objects.filter(title__icontains=search_query)
    
    # If genres are provided in the query, apply the genre filter
    if search_genres:
        genre_list = search_genres.split(',')
        # Construct a single query to include anime that match the search query and contain any of the selected genres
        for genre in genre_list:
            anime_list = anime_list.filter(genre__icontains=genre)

    # Apply additional filters or ordering if needed
    sort_option = request.GET.get('filter')
    if sort_option:
        if sort_option == 'ascending_alpha':
            anime_list = anime_list.order_by('title')
        elif sort_option == 'descending_alpha':
            anime_list = anime_list.order_by('-title')
        elif sort_option == 'popular_first':
            anime_list = anime_list.order_by('-popularity')
        elif sort_option == 'least_popular_first':
            anime_list = anime_list.order_by('popularity')
        elif sort_option == 'more_episodes_first':
            anime_list = anime_list.order_by('-episodes')
        elif sort_option == 'less_episodes_first':
            anime_list = anime_list.order_by('episodes').exclude(episodes=0.0)
        elif sort_option == 'popularity_first':
            anime_list = anime_list.order_by('-popularity')
        elif sort_option == 'least_popularity_first':
            anime_list = anime_list.order_by('popularity')
        elif sort_option == 'rank_first':
            anime_list = anime_list.order_by('-ranked')
        elif sort_option == 'least_rank_first':
            anime_list = anime_list.order_by('ranked').exclude(ranked=0.0)
        elif sort_option == 'air_time':
            anime_list = anime_list.order_by('-aired')
        elif sort_option == 'least_air_time':
            anime_list = anime_list.order_by('aired')
        elif sort_option == 'least_score_first':
            anime_list = anime_list.order_by('score')
        elif sort_option == 'score_first':
            anime_list = anime_list.order_by('-score')
    
    queryCount = anime_list.count()

    # Limit the queryset to 20 results
    anime_list = anime_list[:20]

    # Add star_html attribute to each anime object
    for anime in anime_list:
        anime.star_html = get_star_rating_html(anime.score)  # Assuming you have a function for star rating

    # Pass data to the template
    context = {
        'anime_list': anime_list,
        'search_query': search_query,
        'genres': unique_genres_cache(),  # Assuming you have a function to get unique genres
        'count' : queryCount
    }

    # Render the search.html template with the context data
    return render(request, 'search.html', context)




def fetch_results(request):
    # Get the page number from the request or default to the first page
    page_number = int(request.GET.get('page', 1))
    
    # Get the genre or search query from the request.
    search_query = request.GET.get('query')
    search_genres = request.GET.get('genres')
    
    if search_query:
        # Fetch anime based on the search query
        anime_list = Anime.objects.filter(title__icontains=search_query)
    else:
        # Return an error response if neither genre nor search query is provided
        anime_list = Anime.objects.all()
    
    # If genres are provided, filter anime based on the genres
    if search_genres:
        genre_list = search_genres.split(',')
        for genre in genre_list:
            anime_list = anime_list.filter(genre__icontains=genre)
    
    # Apply ordering by score
    sort_option = request.GET.get('filter')
    if sort_option:
        if sort_option == 'ascending_alpha':
            anime_list = anime_list.order_by('title')
        elif sort_option == 'descending_alpha':
            anime_list = anime_list.order_by('-title')
        elif sort_option == 'popular_first':
            anime_list = anime_list.order_by('-popularity')
        elif sort_option == 'least_popular_first':
            anime_list = anime_list.order_by('popularity')
        elif sort_option == 'more_episodes_first':
            anime_list = anime_list.order_by('-episodes')
        elif sort_option == 'less_episodes_first':
            anime_list = anime_list.order_by('episodes').exclude(episodes=0.0)
        elif sort_option == 'popularity_first':
            anime_list = anime_list.order_by('-popularity')
        elif sort_option == 'least_popularity_first':
            anime_list = anime_list.order_by('popularity')
        elif sort_option == 'rank_first':
            anime_list = anime_list.order_by('-ranked')
        elif sort_option == 'least_rank_first':
            anime_list = anime_list.order_by('ranked').exclude(ranked=0.0)
        elif sort_option == 'air_time':
            anime_list = anime_list.order_by('-aired')
        elif sort_option == 'least_air_time':
            anime_list = anime_list.order_by('aired')
        elif sort_option == 'least_score_first':
            anime_list = anime_list.order_by('score')
        elif sort_option == 'score_first':
            anime_list = anime_list.order_by('-score')
    
    # Calculate start and end indexes for anime based on the page number
    per_page = 20  # Number of anime per page
    offset = 0  
    start_index = (page_number - 1) * per_page + offset
    end_index = start_index + per_page
    
    # Paginate the anime list
    paginated_anime = anime_list[start_index:end_index]
    
    # Serialize the anime objects
    serialized_anime = [{
        'title': anime.title,
        'score': anime.score,
        'img_url': anime.img_url,
        'uid': anime.uid,
        'star_html': get_star_rating_html(anime.score)
        # Add 'star_html' field here if needed
    } for anime in paginated_anime]
    
    if len(paginated_anime) == 0:
        message = 'end'
    else:
        message = 'ok'
        
    # Return the paginated anime as JSON response
    return JsonResponse({'anime_results': serialized_anime, 'message': message})

def about(request):
    # Pass data to the template
    context = {
        'genres': unique_genres_cache()
    }
    
    return render(request, 'about.html', context)
