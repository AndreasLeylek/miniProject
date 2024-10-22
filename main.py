import customtkinter as ctk
from click import command

from TMDB import get_genre_id, get_streaming_provider_id, get_top_250_movies_by_genre, get_popularity_range, \
    get_imdb_id_from_tmdb, get_genre_combination, search_company_by_name, get_company_id
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from web_logger import get_imdb_id_from_tmdb, scrape_imdb_description


# Funktion zum Herunterladen des Posters
def load_poster(url):
    try:
        response = requests.get(url)
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        img = img.resize((300, 400), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)
    except:
        return None


# Popup-Fenster mit den Filmdetails anzeigen
# GUI-Modul für die Anzeige des Popups
def show_movie_popup(movie):
    if movie:
        popup = ctk.CTkToplevel()

        title = movie.get('title')
        release_date = movie.get('release_date', '')[:4] if movie.get('release_date') else 'Unbekannt'

        title_label = ctk.CTkLabel(popup, text=f"{title} ({release_date})", font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=10)

        # Poster anzeigen (wie bereits in deinem Code)
        poster_path = movie.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
        if poster_url:
            poster_img = load_poster(poster_url)
            if poster_img:
                poster_label = ctk.CTkLabel(popup, image=poster_img)
                poster_label.image = poster_img
                poster_label.pack()
            else:
                ctk.CTkLabel(popup, text="Kein Poster verfügbar").pack()

        # IMDb-Beschreibung scrapen und anzeigen
        imdb_id = get_imdb_id_from_tmdb(movie.get('id'))
        description = scrape_imdb_description(imdb_id) if imdb_id else 'Keine IMDb-Beschreibung verfügbar'

        description_label = ctk.CTkLabel(popup, text=f"Beschreibung: {description}", wraplength=400, justify="left")
        description_label.pack(pady=10)

        close_button = ctk.CTkButton(popup, text="Schließen", command=popup.destroy)
        close_button.pack(pady=20)
    else:
        messagebox.showinfo("Fehler", "Kein Film gefunden.")


def scrape_multiple_movie_descriptions(genre_ids, year_group, popularity, streaming_provider_id=None, mood=None,
                                       production_company_id=None):
    movies = get_top_250_movies_by_genre(genre_ids, year_group, popularity, streaming_provider_id, mood,
                                         production_company_id)

    if not movies:
        print("Keine Filme gefunden.")
        return

    # Schritt 2: Für jeden Film die IMDb-ID holen und die IMDb-Beschreibung scrapen
    for movie in movies:
        tmdb_movie_id = movie.get('id')  # TMDb-ID des Films
        title = movie.get('title')  # Titel des Films

        # Schritt 3: IMDb-ID basierend auf der TMDb-ID holen
        imdb_id = get_imdb_id_from_tmdb(tmdb_movie_id)


        if imdb_id:
            # Schritt 4: Scrape IMDb-Beschreibung basierend auf der IMDb-ID
            description = scrape_imdb_description(imdb_id)
            print(f"Film: {title}\nIMDb-ID: {imdb_id}\nBeschreibung: {description}\n")
        else:
            print(f"IMDb-ID für den Film {title} nicht gefunden.")


def update_popularity_label(value):
    popularity_value_label.configure(text=f"Beliebtheit: {int(value)}")


# Hauptfunktion, um die Antworten zu sammeln und den Film zu finden
def on_submit():
    # 1. Benutzereingaben sammeln
    genre = genre_var.get()
    year_group = age_group_var.get().lower()
    mood = mood_var.get()
    streaming_service = streaming_service_var.get()
    production_company_name = production_company_entry.get()
    popularity = popularity_slider.get()
    keywords = keywords_entry.get()
    runtime = runtime_var.get()
    trending = trending_var.get()
    top_rated = top_rated_var.get()

    # 2. Produktionsfirma basierend auf dem Benutzereingang suchen
    selected_company_id = None
    if production_company_name:
        companies = search_company_by_name(production_company_name)
        if companies:
            selected_company_id = companies[0]['id']
            print(f"Gefundene Firma: {companies[0]['name']}, ID: {selected_company_id}")
        else:
            messagebox.showinfo("Fehler", f"Keine Produktionsfirma mit dem Namen '{production_company_name}' gefunden.")

    # 3. Provider-ID für den Streamingdienst finden
    streaming_provider_id = get_streaming_provider_id(streaming_service)
    if not streaming_provider_id:
        messagebox.showinfo("Fehler", "Streamingdienst nicht gefunden.")
        return

    # 4. Popularitätsbereich ermitteln
    popularity_range = get_popularity_range(popularity)

    # 5. Genre-Kombinationen abrufen
    genre_combination = get_genre_combination(genre, mood)

    # 6. Filme suchen
    movies = get_top_250_movies_by_genre(genre_combination, year_group, popularity_range,
                                         streaming_provider_id, mood,
                                         production_company_id=selected_company_id)
    if not movies:
        messagebox.showinfo("Fehler", "Keine Filme gefunden.")
        return

    scrape_multiple_movie_descriptions(genre_combination, year_group, popularity_range,
                                       streaming_provider_id, mood,
                                       production_company_id=selected_company_id)

    # 7. Zeige den ersten Film an
    show_movie_popup(movies[0])



# Funktion zum Aktualisieren der Laufzeitanzeige
def update_runtime_label(value):
    if value == 1:
        runtime_value_label.configure(text="Laufzeit: 0-1 Stunde")
    elif value == 2:
        runtime_value_label.configure(text="Laufzeit: 1-2 Stunden")
    elif value == 3:
        runtime_value_label.configure(text="Laufzeit: 2-3 Stunden")
    elif value == 4:
        runtime_value_label.configure(text="Laufzeit: 3+ Stunden")


# GUI-Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Welchen Film soll ich schauen?")
root.geometry("700x400")

# 1. Genre-Auswahl
ctk.CTkLabel(root, text="Genre").grid(row=0, column=0, padx=10, pady=5)
genre_var = ctk.StringVar(root)
genre_var.set("Action")  # Standardwert setzen
genres = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
          "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
          "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"]
genre_menu = ctk.CTkOptionMenu(root, variable=genre_var, values=genres)
genre_menu.grid(row=0, column=1, padx=10, pady=5)

# 2. Alter (Älter/Neuer)
ctk.CTkLabel(root, text="Alter des Films").grid(row=1, column=0, padx=10, pady=5)
age_group_var = ctk.StringVar(root)
age_group_menu = ctk.CTkOptionMenu(root, variable=age_group_var, values=["Älter", "Neuer", "Keine Angabe"])
age_group_menu.grid(row=1, column=1, padx=10, pady=5)

# 3. Stimmung
ctk.CTkLabel(root, text="Stimmung:").grid(row=2, column=0, padx=10, pady=5)
mood_var = ctk.StringVar(root)
mood_menu = ctk.CTkOptionMenu(root, variable=mood_var,
                              values=["Fröhlich", "Spannend", "Nachdenklich", "Inspirierend", "Krieg",
                                      "Keine Angabe"])
mood_menu.grid(row=2, column=1, padx=10, pady=5)

# 4. Streamingdienst
ctk.CTkLabel(root, text="Streamingdienst").grid(row=3, column=0, padx=10, pady=5)
streaming_service_var = ctk.StringVar(root)
streaming_service_var.set("Netflix")  # Standardwert setzen
streaming_services = ["Netflix", "Amazon Prime", "Disney+", "Hulu", "HBO Max", "Youtube", "Apple TV+", "Sky Go",
                      "Peacock", "Paramount+", "Mubi", "Crave", "Starz"]
streaming_service_menu = ctk.CTkOptionMenu(root, variable=streaming_service_var, values=streaming_services)
streaming_service_menu.grid(row=3, column=1, padx=10, pady=5)

# 5. Produktionsfirma
ctk.CTkLabel(root, text="Produktionsfirma:").grid(row=4, column=0, padx=10, pady=5)
production_company_entry = ctk.CTkEntry(root)
production_company_entry.grid(row=4, column=1, padx=10, pady=5)

# 6. Keywords
ctk.CTkLabel(root, text="Keywords:").grid(row=5, column=0, padx=10, pady=5)
keywords_entry = ctk.CTkEntry(root)
keywords_entry.grid(row=5, column=1, padx=10, pady=5)

# Laufzeit Slider (0-1, 1-2, 2-3, 3+ Stunden)
ctk.CTkLabel(root, text="Laufzeit (Stunden):").grid(row=6, column=0, padx=10, pady=5)
runtime_var = ctk.IntVar()
runtime_slider = ctk.CTkSlider(root, from_=1, to=4, number_of_steps=3, command=update_runtime_label)
runtime_slider.grid(row=6, column=1, padx=10, pady=5)
runtime_value_label = ctk.CTkLabel(root, text="Laufzeit: 0-1 Stunde")
runtime_value_label.grid(row=6, column=2, padx=10, pady=5)

# Beliebtheit (Slider von 1-10)
ctk.CTkLabel(root, text="Beliebtheit ").grid(row=7, column=0, padx=10, pady=5)
popularity_value_label = ctk.CTkLabel(root, text="Beliebtheit: 1")
popularity_value_label.grid(row=7, column=2, padx=10, pady=5)
popularity_slider = ctk.CTkSlider(root, from_=1, to=10, number_of_steps=9, command=update_popularity_label)
popularity_slider.grid(row=7, column=1, padx=10, pady=5)

# Checkboxen untereinander
trending_var = ctk.StringVar(root)
trending_checkbox = ctk.CTkCheckBox(root, text="Aktuell angesagt?", variable=trending_var)
trending_checkbox.grid(row=8, column=0, padx=10, pady=5)

top_rated_var = ctk.StringVar(root)
top_rated_checkbox = ctk.CTkCheckBox(root, text="Sortieren nach Top Rated", variable=top_rated_var)
top_rated_checkbox.grid(row=8, column=1, padx=10, pady=5)

last_results = ctk.CTkButton(root, text="Letzten Ergebnisse", command=on_submit)
last_results.grid(row=8, column=2, padx=10, pady=5)

# Button zum Finden des Films
submit_button = ctk.CTkButton(root, text="Film finden", command=on_submit)
submit_button.grid(row=9, column=2, columnspan=2, pady=20)

root.mainloop()
