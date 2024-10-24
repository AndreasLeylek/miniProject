import webbrowser

import customtkinter as ctk
from TMDB import get_genre_id, get_streaming_provider_id, get_top_250_movies_by_genre, get_popularity_range, \
    get_imdb_id_from_tmdb, get_genre_combination, search_company_by_name, BEARER_TOKEN
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading
from web_logger import scrape_imdb_description


# Funktion zum Herunterladen des Posters
from customtkinter import CTkImage  # Importiere CTkImage

# Funktion zum Herunterladen des Posters und Rückgabe als CTkImage
def load_poster(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Fehlerschutz für HTTP-Fehler
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        img = img.resize((300, 400), Image.Resampling.LANCZOS)

        # Verwende CTkImage statt PIL's PhotoImage
        ctk_image = CTkImage(img, size=(300, 400))  # Angepasste Bildgröße
        return ctk_image
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Laden des Posters: {e}")
        return None
    except Exception as e:
        print(f"Allgemeiner Fehler beim Laden des Posters: {e}")
        return None


def get_streaming_provider_url(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"  # Stelle sicher, dass du hier deinen Token verwendest
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        providers_data = response.json().get('results', {})
        # Prüfen, ob der Film in Deutschland auf Netflix verfügbar ist
        de_providers = providers_data.get('DE', {})
        if 'flatrate' in de_providers:
            for provider in de_providers['flatrate']:
                if provider['provider_name'] == 'Netflix':
                    return "https://www.netflix.com"  # Rückgabe des Netflix-Links oder eines dynamischen Links
        return None
    else:
        print(f"Fehler beim Abrufen der Streaming-Anbieter: {response.status_code}")
        return None


# Funktion zum Abrufen der Streaming-Anbieter (z.B. Netflix)



# Angepasste show_movie_popup Funktion
# Angepasste show_movie_popup Funktion
def show_movie_popup(movie):
    if not movie:
        messagebox.showinfo("Fehler", "Kein Film gefunden.")
        return

    popup = ctk.CTkToplevel()
    popup.title("Filmdetails")
    popup.geometry("600x400")

    title = movie.get('title') or movie.get('original_title') or "Kein Titel verfügbar"
    release_date = movie.get('release_date', '')[:4] if movie.get('release_date') else 'Unbekannt'

    ctk.CTkLabel(popup, text=f"{title} ({release_date})", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

    poster_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None
    if poster_url:
        poster_img = load_poster(poster_url)
        if poster_img:
            poster_label = ctk.CTkLabel(popup, image=poster_img, text="")
            poster_label.image = poster_img  # Verhindert Garbage Collection
            poster_label.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        else:
            ctk.CTkLabel(popup, text="Kein Poster verfügbar").grid(row=1, column=0, padx=10, pady=10)

    imdb_id = get_imdb_id_from_tmdb(movie.get('id'))
    description = scrape_imdb_description(imdb_id) if imdb_id else 'Keine IMDb-Beschreibung verfügbar'
    ctk.CTkLabel(popup, text=f"Beschreibung: {description}", wraplength=250, justify="left").grid(row=1, column=1, padx=10, pady=10, sticky="nw")

    rating = movie.get('vote_average', 'Keine Bewertung verfügbar')
    ctk.CTkLabel(popup, text=f"Bewertung: {rating}/10", font=('Helvetica', 12)).grid(row=2, column=1, padx=10, pady=10, sticky="nw")

    # Streaming-Anbieter abfragen und anzeigen
    streaming_url = get_streaming_provider_url(movie.get('id'))
    if streaming_url:
        ctk.CTkButton(popup, text="Film ansehen", command=lambda: webbrowser.open(streaming_url)).grid(row=3, column=1, padx=10, pady=10, sticky="nw")
    else:
        ctk.CTkLabel(popup, text="Nicht auf Streaming-Plattformen verfügbar").grid(row=3, column=1, padx=10, pady=10, sticky="nw")

    ctk.CTkButton(popup, text="Schließen", command=popup.destroy).grid(row=4, column=0, columnspan=2, pady=20)




def open_url(url):
    webbrowser.open(url)


# Mehrere IMDb-Beschreibungen scrapen
def scrape_multiple_movie_descriptions(genre_ids, year_group, popularity, streaming_provider_id=None, mood=None,
                                       production_company_id=None):
    try:
        movies = get_top_250_movies_by_genre(genre_ids, year_group, popularity, streaming_provider_id, mood,
                                             production_company_id)
        if not movies:
            print("Keine Filme gefunden.")
            return None

        for movie in movies:
            imdb_id = get_imdb_id_from_tmdb(movie.get('id'))
            if imdb_id:
                description = scrape_imdb_description(imdb_id)
                print(f"Film: {movie.get('title')}\nIMDb-ID: {imdb_id}\nBeschreibung: {description}\n")
            else:
                print(f"IMDb-ID für den Film {movie.get('title')} nicht gefunden.")
        return movies[0] if movies else None
    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der API-Abfrage: {e}")
        return None


# API-Aufrufe und GUI-Aktualisierung im Hintergrund durchführen
def perform_api_calls_in_background(loading_window, progress_label, progress_bar, main_window):
    genre = genre_var.get()
    year_group = age_group_var.get().lower()
    mood = mood_var.get()
    streaming_service = streaming_service_var.get()
    production_company_name = production_company_entry.get()
    popularity = popularity_slider.get()

    selected_company_id = None
    if production_company_name:
        companies = search_company_by_name(production_company_name)
        if companies:
            selected_company_id = companies[0]['id']
        else:
            main_window.after(0, lambda: messagebox.showinfo("Fehler", f"Keine Produktionsfirma mit dem Namen '{production_company_name}' gefunden."))
            return

    streaming_provider_id = get_streaming_provider_id(streaming_service)
    if not streaming_provider_id:
        main_window.after(0, lambda: messagebox.showinfo("Fehler", "Streamingdienst nicht gefunden."))
        return

    popularity_range = get_popularity_range(popularity)
    genre_combination = get_genre_combination(genre, mood)

    # Ladebalken starten
    main_window.after(0, lambda: progress_label.configure(text="Lädt..."))
    main_window.after(0, progress_bar.start)

    # API-Aufrufe im Hintergrund
    movie = scrape_multiple_movie_descriptions(genre_combination, year_group, popularity_range, streaming_provider_id,
                                               mood, production_company_id=selected_company_id)

    # Ladebalken stoppen
    main_window.after(0, progress_bar.stop)

    # Ladebalken-Fenster schließen
    main_window.after(0, loading_window.destroy)

    if movie:
        main_window.after(0, lambda: show_movie_popup(movie))


# Funktion zum Erstellen des Ladebalken-Fensters
def show_loading_window(main_window):
    loading_window = ctk.CTkToplevel(main_window)
    loading_window.title("Laden...")  # Titel des Ladefensters
    loading_window.geometry("300x100")

    # Hebe das Ladefenster in den Vordergrund
    loading_window.lift()
    loading_window.attributes('-topmost', True)  # Setzt das Fenster als oberstes
    loading_window.after(1, lambda: loading_window.attributes('-topmost', True))  # Entfernt die "Topmost"-Eigenschaft nach dem Erscheinen

    progress_label = ctk.CTkLabel(loading_window, text="Lädt...", font=("Helvetica", 12))
    progress_label.pack(pady=10)

    progress_bar = ctk.CTkProgressBar(loading_window)
    progress_bar.pack(pady=20)

    # Starte den API-Call in einem Thread
    threading.Thread(target=perform_api_calls_in_background,
                     args=(loading_window, progress_label, progress_bar, main_window)).start()



# Button-Event zum Starten der API-Aufrufe und Anzeige des Ladebalken-Fensters
def start_api_call():
    show_loading_window(main_window)


# Funktion zum Aktualisieren des Popularitäts-Labels
def update_popularity_label(value):
    popularity_value_label.configure(text=f"Beliebtheit: {int(value)}")


# Funktion zum Aktualisieren des Laufzeit-Labels
def update_runtime_label(value):
    runtime_text = ["0-1 Stunde", "1-2 Stunden", "2-3 Stunden", "3+ Stunden"]
    runtime_value_label.configure(text=f"Laufzeit: {runtime_text[int(value) - 1]}")


# GUI-Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

main_window = ctk.CTk()
main_window.title("Filmfinder")
main_window.geometry("700x400")

# GUI-Elemente erstellen
ctk.CTkLabel(main_window, text="Genre").grid(row=0, column=0, padx=10, pady=5)
genre_var = ctk.StringVar(main_window)
genre_var.set("Action")
genres = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
          "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
          "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"]
ctk.CTkOptionMenu(main_window, variable=genre_var, values=genres).grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(main_window, text="Alter des Films").grid(row=1, column=0, padx=10, pady=5)
age_group_var = ctk.StringVar(main_window)
ctk.CTkOptionMenu(main_window, variable=age_group_var, values=["Älter", "Neuer", "Keine Angabe"]).grid(row=1, column=1,
                                                                                                        padx=10, pady=5)

ctk.CTkLabel(main_window, text="Stimmung:").grid(row=2, column=0, padx=10, pady=5)
mood_var = ctk.StringVar(main_window)
ctk.CTkOptionMenu(main_window, variable=mood_var,
                  values=["Fröhlich", "Spannend", "Nachdenklich", "Inspirierend", "Krieg", "Keine Angabe"]).grid(row=2,
                                                                                                                 column=1,
                                                                                                                 padx=10,
                                                                                                                 pady=5)

ctk.CTkLabel(main_window, text="Streamingdienst").grid(row=3, column=0, padx=10, pady=5)
streaming_service_var = ctk.StringVar(main_window)
streaming_service_var.set("Netflix")
streaming_services = ["Netflix", "Amazon Prime", "Disney+", "Hulu", "HBO Max", "Youtube", "Apple TV+", "Sky Go",
                      "Peacock", "Paramount+", "Mubi", "Crave", "Starz"]
ctk.CTkOptionMenu(main_window, variable=streaming_service_var, values=streaming_services).grid(row=3, column=1, padx=10,
                                                                                                pady=5)

ctk.CTkLabel(main_window, text="Produktionsfirma:").grid(row=4, column=0, padx=10, pady=5)
production_company_entry = ctk.CTkEntry(main_window)
production_company_entry.grid(row=4, column=1, padx=10, pady=5)

ctk.CTkLabel(main_window, text="Laufzeit (Stunden):").grid(row=5, column=0, padx=10, pady=5)
runtime_var = ctk.IntVar()
runtime_slider = ctk.CTkSlider(main_window, from_=1, to=4, number_of_steps=3, command=update_runtime_label)
runtime_slider.grid(row=5, column=1, padx=10, pady=5)
runtime_value_label = ctk.CTkLabel(main_window, text="Laufzeit: 0-1 Stunde")
runtime_value_label.grid(row=5, column=2, padx=10, pady=5)

ctk.CTkLabel(main_window, text="Beliebtheit").grid(row=6, column=0, padx=10, pady=5)
popularity_value_label = ctk.CTkLabel(main_window, text="Beliebtheit: 1")
popularity_value_label.grid(row=6, column=2, padx=10, pady=5)
popularity_slider = ctk.CTkSlider(main_window, from_=1, to=10, number_of_steps=9, command=update_popularity_label)
popularity_slider.grid(row=6, column=1, padx=10, pady=5)

trending_var = ctk.StringVar(main_window)
ctk.CTkCheckBox(main_window, text="Aktuell angesagt?", variable=trending_var).grid(row=7, column=0, padx=10, pady=5)

top_rated_var = ctk.StringVar(main_window)
ctk.CTkCheckBox(main_window, text="Sortieren nach Top Rated", variable=top_rated_var).grid(row=7, column=1, padx=10, pady=5)

# Button zum Starten der API-Aufrufe
submit_button = ctk.CTkButton(main_window, text="Film finden", command=start_api_call)
submit_button.grid(row=9, column=2, columnspan=2, pady=20)

main_window.mainloop()
