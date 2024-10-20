import requests

BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlOWZjZGIxYTM5YTY3OWIzNzA2MTkyMTNjYTg1ODJlZSIsIm5iZiI6MTcyOTQyNTc5OC41MzYwNTIsInN1YiI6IjY3MGUyNDAyOWYzNTMxZTZiMjZjNTdlMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AGTtZT0CKAOXG-lmogUqX30N2ErkQeULnpC6Z8wUCxo"

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



def get_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    params = {
        "language": "de"  # Sprache auf Deutsch setzen
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
        "watch_region": "DE"  # Region (DE für Deutschland)
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
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



def get_top_250_movies_by_genre(genre_id, year_group, popularity, streaming_provider_id=None):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    all_movies = []
    current_page = 1
    total_pages = 13  # Da jede Seite 20 Filme enthält (13 * 20 = 260)

    while len(all_movies) < 250 and current_page <= total_pages:
        params = {
            "with_genres": genre_id,
            "sort_by": "popularity.desc" if popularity == "bekannt" else "popularity.asc",
            "page": current_page,
            "language": "de",
            "region": "DE"
        }

        # Älter oder neuer Film (Jahr filtern)
        if year_group == "älter":
            params["release_date.lte"] = "2000-01-01"
        else:
            params["release_date.gte"] = "2000-01-01"

        # Optional: Filter nach Streamingdienst
        if streaming_provider_id:
            params["with_watch_providers"] = streaming_provider_id
            params["watch_region"] = "DE"  # Stelle sicher, dass es für Deutschland gefiltert wird

        url = "https://api.themoviedb.org/3/discover/movie"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            movies = response.json().get("results", [])
            all_movies.extend(movies)
        else:
            print(f"Fehler bei der API-Abfrage: {response.status_code}")
            break

        current_page += 1

    return all_movies[:250]  # Nur die Top 250 zurückgeben
