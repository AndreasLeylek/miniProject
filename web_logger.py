import requests
from bs4 import BeautifulSoup


# Web Scraping, um die Metascore-Bewertung von Metacritic zu erhalten
def get_metascore(movie_title):
    search_url = f"https://www.metacritic.com/search/all/{movie_title}/results"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Versuch die Metascore zu scrapen (dies muss eventuell angepasst werden)
    try:
        metascore = soup.find('span', class_='metascore_w').text
        return metascore
    except AttributeError:
        return "Metascore nicht verfügbar"
