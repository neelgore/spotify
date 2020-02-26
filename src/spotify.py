import requests
from classes import Track, Artist, Album
from keys import USER_ID, OAUTH_TOKEN

def get_playlist(playlist_id: str) -> dict:
    query = "https://api.spotify.com/v1/playlists/{}".format(playlist_id)
    response = requests.get(query, headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(OAUTH_TOKEN)})
    return response.json()

def get_artist_albums(artist_id: str) -> dict:
    query = "https://api.spotify.com/v1/artists/{}/albums".format(artist_id)
    params = {"limit": 50, "offset": 100}
    response = requests.get(query, params, headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(OAUTH_TOKEN)})
    return response.json()


if __name__ == "__main__":
    albums = get_artist_albums("45eNHdiiabvmbp4erw26rg")
    print(len(albums))
