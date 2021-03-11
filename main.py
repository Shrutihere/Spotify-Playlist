
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

SPOTIFY_ID = "9b30badd4397415298b1edd08d20e737"
SPOTIFY_SECRET= "96a288b03e0e49bbaf1f9fb8bbefdbd5"
URL = "https://www.billboard.com/charts/hot-100/"
date = input("Which year do you want to travel to? Type in YYYY-MM-DD format: ")
contents = requests.get(f"{URL}{date}")
soup = BeautifulSoup(contents.text, 'html.parser')
song_tags = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")
song_list = []
for song in song_tags:
    song_list.append(song.string)

auth = SpotifyOAuth(client_id=SPOTIFY_ID,
                    client_secret=SPOTIFY_SECRET,
                    redirect_uri="http://example.com",
                    scope="playlist-modify-private",
                    show_dialog=True,
                    cache_path="token.txt",
                    open_browser=True
                            )
spotify = spotipy.Spotify(auth_manager=auth)
user_id = spotify.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_list:
    result = spotify.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

print(song_uris)

playlist = spotify.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

spotify.playlist_add_items(playlist_id=playlist["id"], items=song_uris)





