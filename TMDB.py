import requests
import random

BEARER_TOKEN = (
    "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlOWZjZGIxYTM5YTY3OWIzNzA2MTkyMTNjYTg1ODJlZSIsIm5iZiI6MTcyOTUwMTU2MC42NzYxOTMsInN1YiI6IjY3MGUyNDAyOWYzNTMxZTZiMjZjNTdlMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9jM6bs1v8fcVTvS8b91n0OP4lYn0yuzuWVZcdQI2x1c")


def get_genre_id(genre_name):
    url = "https://api.themoviedb.org/3/genre/movie/list"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.json())

    if genre_name.lower() == "action":
        return 28
    elif genre_name.lower() == "adventure":
        return 12
    elif genre_name.lower() == "animation":
        return 16
    elif genre_name.lower() == "comedy":
        return 35
    elif genre_name.lower() == "crime":
        return 80
    elif genre_name.lower() == "documentary":
        return 99
    elif genre_name.lower() == "drama":
        return 18
    elif genre_name.lower() == "family":
        return 10751
    elif genre_name.lower() == "fantasy":
        return 14
    elif genre_name.lower() == "history":
        return 36
    elif genre_name.lower() == "horror":
        return 27
    elif genre_name.lower() == "music":
        return 10402
    elif genre_name.lower() == "mystery":
        return 9648
    elif genre_name.lower() == "romance":
        return 10749
    elif genre_name.lower() == "science fiction":
        return 878
    elif genre_name.lower() == "tv movie":
        return 10770
    elif genre_name.lower() == "thriller":
        return 53
    elif genre_name.lower() == "war":
        return 10752
    elif genre_name.lower() == "western":
        return 37
    else:
        return None  # Falls kein passendes Genre gefunden wird


def get_company_id(company_name):
    url = f"https://api.themoviedb.org/3/search/company"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    params = {
        "query": "Doorsproduction"  # Hier den Firmennamen eingeben, z.B. "Doors Production"
    }

    # API-Anfrage, um die Produktionsfirma zu suchen
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        companies = response.json().get("results", [])
        if companies:
            # Gibt die erste gefundene Company-ID zurück
            return companies[0].get("id")
        else:
            print(f"Keine Firma mit dem Namen '{company_name}' gefunden.")
            return None
    else:
        print(f"Fehler bei der API-Abfrage: {response.status_code}")
        return None


def get_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    params = {
        "language": "de-DE",  # Sprache auf Deutsch setzen
        "watch_region": "de-DE"
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("genres", [])
    else:
        print(f"Fehler bei der API-Abfrage: {response.status_code}")
        return []


def get_streaming_providers():
    url = "https://api.themoviedb.org/3/watch/providers/movie"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    params = {
        "language": "de",  # Spracheinstellung
        "watch_region": "DE"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Fehler bei der API-Abfrage: {response.status_code}")
        return []


# Mapping von Genre und Stimmung auf spezifische Genre-Kombinationen
def get_genre_combination(genre, mood):
    genre_map = {
        'Action': {
            'Fröhlich': [28, 35],  # Action + Comedy
            'Spannend': [28, 53],  # Action + Thriller
            'Nachdenklich': [28, 18],  # Action + Drama
            'Inspirierend': [28, 12],  # Action + Adventure
            'Liebe': [28, 10749],  # Action + Romance
            'Psycho': [28, 27],  # Action + Horror
            'Krieg': [28, 10752]  # Action + War
        },
        'Science Fiction': {
            'Fröhlich': [878, 35],  # Science Fiction + Comedy
            'Spannend': [878, 53],  # Science Fiction + Thriller
            'Nachdenklich': [878, 18],  # Science Fiction + Drama
            'Inspirierend': [878, 12]  # Science Fiction + Adventure
        },
        'Adventure': {
            'Fröhlich': [12, 35],  # Adventure + Comedy
            'Spannend': [12, 53]  # Adventure + Thriller
        },
        # Weitere Genre-Definitionen kannst du hier hinzufügen...
    }

    # Rückgabe der kombinierten Genres basierend auf Stimmung und Hauptgenre
    if genre in genre_map and mood in genre_map[genre]:
        return genre_map[genre][mood]
    else:
        # Falls keine Stimmung definiert ist, nur das Hauptgenre verwenden
        return [get_genre_id(genre)]


def search_company_by_name(company_name):
    if not company_name or not company_name.strip():
        print("Kein Firmenname angegeben.")
        return []
    url = "https://api.themoviedb.org/3/search/company"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    params = {
        "query": company_name
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        companies = response.json().get("results", [])
        if companies:
            return companies
        else:
            print(f"Keine Firmen mit dem Namen '{company_name}' gefunden.")
            return []
    else:
        print(f"Fehler bei der API-Abfrage: {response.status_code}")
        return []


# Funktion, um Popularitätsbereiche basierend auf der Slider-Position zu ermitteln
def get_popularity_range(slider_value):
    if slider_value == 1:
        return (0, 20)
    elif slider_value == 2:
        return (20, 40)
    elif slider_value == 3:
        return (40, 60)
    elif slider_value == 4:
        return (60, 80)
    elif slider_value == 5:
        return (80, 100)
    elif slider_value == 6:
        return (100, 150)
    elif slider_value == 7:
        return (150, 200)
    elif slider_value == 8:
        return (200, 300)
    elif slider_value == 9:
        return (300, 500)
    elif slider_value == 10:
        return (500, None)  # Unbegrenzte Popularität


import requests


def get_imdb_id_from_tmdb(tmdb_movie_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_movie_id}"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        movie_data = response.json()
        imdb_id = movie_data.get("imdb_id")
        if imdb_id:
            return imdb_id
        else:
            print("Keine IMDb-ID gefunden.")
            return None
    else:
        print(f"Fehler bei der API-Anfrage: {response.status_code}")
        return None


def get_streaming_provider_id(streaming_service_name):
    if streaming_service_name.lower() == "netflix":
        return 8
    elif streaming_service_name.lower() == "amazon prime":
        return 9
    elif streaming_service_name.lower() == "disney+":
        return 337
    elif streaming_service_name.lower() == "hulu":
        return 15
    elif streaming_service_name.lower() == "hbo max":
        return 384
    elif streaming_service_name.lower() == "apple itunes":
        return 2
    elif streaming_service_name.lower() == "google play movies":
        return 3
    elif streaming_service_name.lower() == "youtube":
        return 188
    elif streaming_service_name.lower() == "apple tv+":
        return 350
    elif streaming_service_name.lower() == "sky go":
        return 19
    elif streaming_service_name.lower() == "peacock":
        return 386
    elif streaming_service_name.lower() == "paramount+":
        return 531
    elif streaming_service_name.lower() == "mubi":
        return 421
    elif streaming_service_name.lower() == "crave":
        return 230
    elif streaming_service_name.lower() == "starz":
        return 43
    else:
        return None


def get_top_250_movies_by_genre(genre_ids, year_group, popularity, streaming_provider_id=None, mood=None,
                                production_company_id=None):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    all_movies = []
    current_page = 1
    max_returned_movies = 10
    genre_ids_str = ",".join(map(str, genre_ids))

    while len(all_movies) < max_returned_movies:
        params = {
            "with_genres": genre_ids_str,
            "language": "de-DE",
            "page": current_page
        }

        # Ältere oder neuere Filme filtern
        if year_group == "älter":
            params["release_date.lte"] = "2000-01-01"
        elif year_group == "neuer":
            params["release_date.gte"] = "2000-01-01"

        # Produktionsfirma ID hinzufügen, falls vorhanden
        if production_company_id:
            params["with_companies"] = production_company_id

        # Filter nach Streamingdienst (falls angegeben)
        if streaming_provider_id:
            params["with_watch_providers"] = streaming_provider_id
            params["watch_region"] = "DE"

        # Sortierung basierend auf Popularität
        params["sort_by"] = "popularity.desc" if popularity == "bekannt" else "popularity.asc"

        # API-Anfrage
        url = "https://api.themoviedb.org/3/discover/movie"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            response_data = response.json()
            movies = response_data.get("results", [])
            total_pages = response_data.get("total_pages", 1)

            for movie in movies:
                imdb_id = get_imdb_id_from_tmdb(movie.get('id'))
                if imdb_id:
                    title = movie.get('title') or movie.get('original_title')
                    print(f"Film: {title}, IMDb-ID: {imdb_id}")
                    all_movies.append(movie)

            if current_page >= total_pages:
                break

            current_page += 1
        else:
            print(f"Fehler bei der API-Abfrage: {response.status_code}")
            break

    if len(all_movies) > 0:
        random_movies = random.sample(all_movies, min(len(all_movies), max_returned_movies))
    else:
        random_movies = []

    return random_movies

