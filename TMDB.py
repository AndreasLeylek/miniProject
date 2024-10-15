import requests
from API_KEY_URL import *
from bs4 import BeautifulSoup

# Bearer Token für TMDb API

BEARER_TOKEN = {BEARER_TOKEN}
BASE_URL = {BASE_URL}

# Funktion, um Fragen an den Benutzer zu stellen und die Antworten zu sammeln
def ask_questions():
    genre = input("In welchem Genre befindet sich der Film? (z.B. Action, Comedy, Drama, Horror): ").capitalize()
    age_group = input(
        "Möchtest du einen älteren oder neueren Film sehen? (älter = vor 2000, neuer = ab 2000): ").lower()
    actor = input(
        "Gibt es einen Schauspieler oder eine Schauspielerin, den/die du bevorzugst? (optional, einfach Enter drücken, wenn keine Präferenz): ").capitalize()
    popular = input(
        "Möchtest du eher einen bekannten oder nicht so bekannten Film anschauen? (bekannt/nicht bekannt): ").lower()
    top_rated = input("Möchtest du die Top Ratings aus einer Genre holen? (ja/nein): ").lower()
    user_rating = input("Vertraust du lieber Benutzerbewertungen? (ja/nein): ").lower()
    based_other_movie = input(
        "Gibt es einen Film, den du gut findest? Dann kann ich ähnliche Filme vorschlagen (optional): ").capitalize()

    return genre, age_group, actor, popular, top_rated, user_rating, based_other_movie


# Funktion, um die Details eines Films basierend auf der Film-ID abzurufen
def get_movie_details(movie_id):
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }
    details_url = f"{BASE_URL}/movie/{movie_id}"

    response = requests.get(details_url, headers=headers)

    if response.status_code == 404:
        return None  # Gib None zurück, wenn der Film nicht gefunden wird

    if response.status_code != 200:
        return None  # Gib None zurück bei anderen Fehlern

    return response.json()


# Funktion zum Anzeigen von Filminformationen, inklusive Poster-URL
def display_movie_info(movie):
    print(
        f"- {movie['title']} ({movie['release_date'][:4] if movie.get('release_date') else 'Kein Datum'}) - Bewertung: {movie.get('vote_average', 'Keine Bewertung')}")

    # Genre anzeigen
    genres = movie.get('genres', [])
    if genres:
        print(f"   Genre: {', '.join([g['name'] for g in genres])}")
    else:
        print("   Genre: Keine Informationen verfügbar")

    # Handlung anzeigen
    print(f"   Handlung: {movie.get('overview', 'Keine Handlung verfügbar')}")

    # Poster-URL generieren und anzeigen
    poster_path = movie.get('poster_path')
    if poster_path:
        # Generiere die vollständige Poster-URL
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        print(f"   Poster: {poster_url}")
    else:
        print("   Poster: Kein Poster verfügbar")
    print()


# Funktion, um ähnliche Filme basierend auf einem Filmvorschlag zu suchen
def search_similar_movies(movie_title):
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }
    # Suche die Movie-ID basierend auf dem Titel des Films
    search_url = f"{BASE_URL}/search/movie"
    params = {'query': movie_title}
    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code != 200:
        return []  # Gib eine leere Liste zurück, falls die Suche fehlschlägt

    data = response.json().get('results', [])

    if not data:
        return []  # Gib eine leere Liste zurück, wenn der Film nicht gefunden wurde

    movie_id = data[0]['id']
    # Suche ähnliche Filme basierend auf der Movie-ID
    similar_url = f"{BASE_URL}/movie/{movie_id}/similar"
    response = requests.get(similar_url, headers=headers)

    if response.status_code != 200:
        return []  # Gib eine leere Liste zurück, wenn die ähnliche Filme nicht gefunden werden

    return response.json().get('results', [])


# Funktion, um Filme basierend auf den Antworten zu suchen
def search_movie(genre, age_group, actor, popular, top_rated, user_rating):
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }
    params = {'query': actor if actor else genre}  # Nutze Schauspieler oder Genre als Suchparameter
    search_url = f"{BASE_URL}/search/movie"

    # Anfrage an die TMDb API senden
    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code != 200:
        return []  # Gib eine leere Liste zurück, falls die Suche fehlschlägt

    return response.json().get('results', [])


