import requests
import random

BEARER_TOKEN = (
    "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlOWZjZGIxYTM5YTY3OWIzNzA2MTkyMTNjYTg1ODJlZSIsIm5iZiI6MTcyOTUwMTU2MC42NzYxOTMsInN1YiI6IjY3MGUyNDAyOWYzNTMxZTZiMjZjNTdlMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9jM6bs1v8fcVTvS8b91n0OP4lYn0yuzuWVZcdQI2x1c"
)

API_BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}


# Hilfsfunktion für API-Anfragen
def make_request(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler bei der API-Abfrage: {response.status_code}")
        return None


# Genre-ID basierend auf Namen zurückgeben
def get_genre_id(genre_name):
    genres = {
        "action": 28,
        "adventure": 12,
        "animation": 16,
        "comedy": 35,
        "crime": 80,
        "documentary": 99,
        "drama": 18,
        "family": 10751,
        "fantasy": 14,
        "history": 36,
        "horror": 27,
        "music": 10402,
        "mystery": 9648,
        "romance": 10749,
        "science fiction": 878,
        "tv movie": 10770,
        "thriller": 53,
        "war": 10752,
        "western": 37,
    }
    return genres.get(genre_name.lower(), None)


# Produktionsfirma basierend auf Namen suchen
def get_company_id(company_name):
    url = f"{API_BASE_URL}/search/company"
    params = {"query": company_name}
    response_data = make_request(url, params)
    if response_data:
        companies = response_data.get("results", [])
        if companies:
            return companies[0].get("id")
        else:
            print(f"Keine Firma mit dem Namen '{company_name}' gefunden.")
    return None


# Alle verfügbaren Genres abrufen
def get_genres():
    url = f"{API_BASE_URL}/genre/movie/list"
    params = {"language": "de-DE"}
    return make_request(url, params).get("genres", [])


# Streaming-Provider abrufen
def get_streaming_providers():
    url = f"{API_BASE_URL}/watch/providers/movie"
    params = {"language": "de", "watch_region": "DE"}
    return make_request(url, params).get("results", [])


# Genre-Kombinationen basierend auf Genre und Stimmung
def get_genre_combination(genre, mood):
    genre_map = {
        "Action": {
            "Fröhlich": [28, 35],
            "Spannend": [28, 53],
            "Nachdenklich": [28, 18],
            "Inspirierend": [28, 12],
            "Liebe": [28, 10749],
            "Psycho": [28, 27],
            "Krieg": [28, 10752],
        },
        "Science Fiction": {
            "Fröhlich": [878, 35],
            "Spannend": [878, 53],
            "Nachdenklich": [878, 18],
            "Inspirierend": [878, 12],
        },
        "Adventure": {
            "Fröhlich": [12, 35],
            "Spannend": [12, 53],
        },
    }
    return genre_map.get(genre, {}).get(mood, [get_genre_id(genre)])


# Produktionsfirma nach Namen suchen
def search_company_by_name(company_name):
    if not company_name.strip():
        print("Kein Firmenname angegeben.")
        return []
    url = f"{API_BASE_URL}/search/company"
    params = {"query": company_name}
    return make_request(url, params).get("results", [])


# Popularitätsbereich auf Basis des Slider-Werts
def get_popularity_range(slider_value):
    ranges = {
        1: (0, 20),
        2: (20, 40),
        3: (40, 60),
        4: (60, 80),
        5: (80, 100),
        6: (100, 150),
        7: (150, 200),
        8: (200, 300),
        9: (300, 500),
        10: (500, None),
    }
    return ranges.get(slider_value)


# IMDb-ID basierend auf der TMDb-ID abrufen
def get_imdb_id_from_tmdb(tmdb_movie_id):
    url = f"{API_BASE_URL}/movie/{tmdb_movie_id}"
    movie_data = make_request(url)
    if movie_data:
        return movie_data.get("imdb_id")
    print("Keine IMDb-ID gefunden.")
    return None


# Streaming-Provider-ID basierend auf Namen abrufen
def get_streaming_provider_id(streaming_service_name):
    provider_map = {
        "netflix": 8,
        "amazon prime": 9,
        "disney+": 337,
        "hulu": 15,
        "hbo max": 384,
        "apple itunes": 2,
        "google play movies": 3,
        "youtube": 188,
        "apple tv+": 350,
        "sky go": 19,
        "peacock": 386,
        "paramount+": 531,
        "mubi": 421,
        "crave": 230,
        "starz": 43,
    }
    return provider_map.get(streaming_service_name.lower())



def get_streaming_provider_url(movie_id):
    url = f"/3/movie/:movie_id/watch/providers?={movie_id}"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"  # Stelle sicher, dass du hier deinen Token verwendest
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        providers_data = response.json().get('results', {})
        de_providers = providers_data.get('DE', {})  # Für Deutschland (kannst die Region ändern)

        if 'flatrate' in de_providers:
            # Liste für bekannte Streaming-Anbieter und ihre URL-Formate
            streaming_links = {
                "Netflix": "https://www.netflix.com",
                "Amazon Prime Video": "https://www.primevideo.com",
                "Disney Plus": "https://www.disneyplus.com",
                "Hulu": "https://www.hulu.com",
                "HBO Max": "https://www.hbomax.com",
                "Apple iTunes": "https://www.apple.com/itunes",
                "Google Play Movies": "https://play.google.com/store/movies",
                "YouTube": "https://www.youtube.com",
                "Sky Go": "https://www.sky.de",
                "Peacock": "https://www.peacocktv.com",
                "Paramount+": "https://www.paramountplus.com",
                "Mubi": "https://mubi.com",
                "Crave": "https://www.crave.ca",
                "Starz": "https://www.starz.com"
            }

            # Suche nach dem Provider in der Antwort
            for provider in de_providers['flatrate']:
                provider_name = provider['provider_name']
                if provider_name in streaming_links:
                    return streaming_links[provider_name]  # Rückgabe des jeweiligen Links

        return None  # Falls kein Provider gefunden wurde
    else:
        print(f"Fehler beim Abrufen der Streaming-Anbieter: {response.status_code}")
        return None


# Top 250 Filme basierend auf Genre und Filtern abrufen
def get_top_250_movies_by_genre(genre_ids, year_group, popularity, streaming_provider_id=None, mood=None,
                                production_company_id=None):
    url = f"{API_BASE_URL}/discover/movie"
    genre_ids_str = ",".join(map(str, genre_ids))
    all_movies = []
    current_page = 1
    max_returned_movies = 10

    while len(all_movies) < max_returned_movies:
        params = {
            "with_genres": genre_ids_str,
            "language": "de-DE",
            "page": current_page,
            "sort_by": "popularity.desc" if popularity == "bekannt" else "popularity.asc",
        }

        # Filter nach Älter/Neuer
        if year_group == "älter":
            params["release_date.lte"] = "2000-01-01"
        elif year_group == "neuer":
            params["release_date.gte"] = "2000-01-01"

        # Filter nach Produktionsfirma und Streaminganbieter
        if production_company_id:
            params["with_companies"] = production_company_id
        if streaming_provider_id:
            params["with_watch_providers"] = streaming_provider_id
            params["watch_region"] = "DE"

        response_data = make_request(url, params)
        if response_data:
            movies = response_data.get("results", [])
            total_pages = response_data.get("total_pages", 1)

            for movie in movies:
                imdb_id = get_imdb_id_from_tmdb(movie.get("id"))
                if imdb_id:
                    title = movie.get("title") or movie.get("original_title")
                    print(f"Film: {title}, IMDb-ID: {imdb_id}")
                    all_movies.append(movie)

            if current_page >= total_pages:
                break
            current_page += 1
        else:
            break

    return random.sample(all_movies, min(len(all_movies), max_returned_movies)) if all_movies else []
