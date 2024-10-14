import requests

# API-Schlüssel und URL für OMDb API
API_KEY = '849cfc60'
URL = 'http://www.omdbapi.com/'


# Funktion, um Fragen an den Benutzer zu stellen und die Antworten zu sammeln
def ask_questions():
    genre = input("In welchem Genre befindet sich der Film? (z.B. Action, Comedy, Drama, Horror): ").capitalize()
    age_group = input(
        "Möchtest du einen älteren oder neueren Film sehen? (älter = vor 2000, neuer = ab 2000): (optional, einfach Enter drücken, wenn keine Präferenz) ").lower()
    actor = input(
        "Gibt es einen Schauspieler oder eine Schauspielerin, den/die du bevorzugst? (optional, einfach Enter drücken, wenn keine Präferenz): ").capitalize()

    return genre, age_group, actor


# Funktion, um nach Filmen basierend auf Benutzerantworten zu suchen
def search_movie(genre, age_group, actor):
    params = {
        'apikey': API_KEY,
        'type': 'movie',  # Nur Filme suchen
        's': genre  # Suche nach Genre
    }

    # Optional: Nur hinzufügen, wenn der Schauspieler eingegeben wurde
    if actor:
        params['s'] = actor  # Nach Schauspieler suchen, wenn angegeben

    # Anfrage an die OMDb API senden
    response = requests.get(URL, params=params)

    # Überprüfen, ob die Anfrage erfolgreich war (HTTP-Statuscode)
    if response.status_code != 200:
        print("Fehler bei der API-Anfrage:", response.status_code)
        return []

    # API-Daten in JSON umwandeln
    data = response.json()

    # Überprüfen, ob Filme gefunden wurden
    if data.get('Response') == 'True':
        print(f"{len(data['Search'])} Filme gefunden.")

        # Optionales Genre-Filtering im Code, wenn Genre eingegeben wurde
        filtered_movies = []
        for movie in data['Search']:
            # Ruft für jeden Film die Details ab
            details = get_movie_details(movie['imdbID'])
            runtime = details.get('Runtime', '')

            # Überprüfen, ob die Laufzeit eine Zahl enthält
            try:
                runtime_in_minutes = int(runtime.split()[0]) if runtime and runtime != 'N/A' else 0
            except ValueError:
                print(f"Ungültige Laufzeit für den Film '{details['Title']}': {runtime}")
                runtime_in_minutes = 0  # Falls die Laufzeit nicht in Minuten ist, setzen wir sie auf 0

            print(
                f"Überprüfe Film: {details['Title']} mit Genre: {details.get('Genre', 'Kein Genre')}, Laufzeit: {runtime}, Jahr: {details['Year']}")

            # Prüfen, ob das Genre enthalten ist (flexible Filterung, keine exakte Übereinstimmung nötig)
            if genre.lower() not in details.get('Genre', '').lower():
                print(f"Film '{details['Title']}' hat das Genre {details['Genre']}, passt aber nicht exakt.")
                continue

            # Prüfen, ob der Film in die richtige Alterskategorie fällt (wenn angegeben)
            year = int(details.get('Year', '0').split('–')[0])  # Manchmal gibt es "1999–" für Serien, deshalb splitten
            if age_group == 'älter' and year >= 2000:
                print(f"Film '{details['Title']}' ist kein älterer Film.")
                continue
            elif age_group == 'neuer' and year < 2000:
                print(f"Film '{details['Title']}' ist kein neuerer Film.")
                continue

            # Prüfen, ob es sich um einen Kurzfilm handelt (Laufzeit unter 60 Minuten)
            if runtime_in_minutes < 60:
                print(f"Film '{details['Title']}' ist ein Kurzfilm und wird nicht berücksichtigt.")
                continue

            filtered_movies.append(details)

        # Rückgabe der Top 10 Filme in diesem Genre, wenn keine Alters- oder Schauspieler-Filter angewendet werden
        if not age_group and not actor:
            return filtered_movies[:10]  # Top 10 zurückgeben

        return filtered_movies
    else:
        print("Keine passenden Filme gefunden.")
        return []


# Funktion, um die Details eines Films basierend auf der IMDb-ID abzurufen
def get_movie_details(imdb_id):
    params = {
        'apikey': API_KEY,
        'i': imdb_id
    }
    response = requests.get(URL, params=params)

    # Fehlerbehandlung für die Abfrage der Details
    if response.status_code != 200:
        print(f"Fehler bei der Detail-Abfrage (IMDb-ID: {imdb_id}):", response.status_code)
        return {}

    return response.json()


# Hauptprogramm (Main-Klasse), die den gesamten Ablauf steuert
def main():
    # 1. Fragen an den Benutzer stellen und Antworten sammeln
    genre, age_group, actor = ask_questions()

    # 2. Suche nach Filmen basierend auf den Antworten
    movies = search_movie(genre, age_group, actor)

    # 3. Gefundene Filme anzeigen
    if movies:
        print(f"\nGefundene Filme:")
        for movie in movies:
            print(f"- {movie['Title']} ({movie['Year']}) - Bewertung: {movie.get('imdbRating', 'Keine Bewertung')}")
            print(f"   Genre: {movie['Genre']}")
            print(f"   Handlung: {movie['Plot']}")
            print()
    else:
        print("Es wurden keine Filme gefunden.")


# Programm starten
if __name__ == "__main__":
    main()
