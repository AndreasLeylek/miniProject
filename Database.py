import psycopg2
import requests

# Funktion zur Herstellung der Datenbankverbindung
def connect_to_db():
    try:
        # Verbindung zur Datenbank herstellen
        connection = psycopg2.connect(
            host="localhost",
            database="TMDB",
            user="postgres",
            password="codersbay"
        )
        return connection
    except Exception as e:
        print(f"Fehler bei der Verbindung zur Datenbank: {e}")
        return None


import requests
import psycopg2


# Abrufen der Filmdaten von TMDB
def get_movie_data_from_tmdb(movie_id):
    BEARER_TOKEN = "your_tmdb_bearer_token"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        movie_data = response.json()

        # Extrahieren des Jahres aus release_date (wenn vorhanden)
        release_date = movie_data.get('release_date', None)
        release_year = None
        if release_date:
            release_year = release_date.split("-")[0]  # Nur das Jahr extrahieren

        # Rückgabe des Movie-Datensatzes
        movie_data['release_year'] = release_year
        return movie_data
    else:
        print(f"Fehler: {response.status_code}")
        return None


# Funktion zum Einfügen der Daten in die Datenbank
def insert_movie_into_db(movie_data):
    connection = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # SQL-Insert-Anweisung für die Movies-Tabelle
        insert_query = """
        INSERT INTO Movies (id, title, release_year, imdb_id, description)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """

        # Daten für das Einfügen vorbereiten
        movie_id = movie_data['id']
        title = movie_data['title']
        release_year = movie_data.get('release_year', None)
        imdb_id = movie_data.get('imdb_id', None)
        description = movie_data.get('overview', '')

        # Einfügen der Daten in die Tabelle
        cursor.execute(insert_query, (movie_id, title, release_year, imdb_id, description))
        connection.commit()  # Änderungen in der DB speichern

        print(f"Film {title} erfolgreich in die Datenbank eingefügt.")

    except Exception as e:
        print(f"Fehler beim Einfügen in die Datenbank: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()  # Schließe die Datenbankverbindung
