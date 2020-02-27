import requests
from classes import Track, Artist, Album

ARTISTS = set()
OAUTH_TOKEN = open("key.txt").readline()
HEADERS = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(OAUTH_TOKEN)}


class KeyExpiredError(Exception):
    pass

def get_playlist_tracks(playlist_id: str) -> [Track]:
    tracks = []
    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
    page = 0
    params = {"limit": 50, "offset": 50*page}
    #playlist track object has a track object in "items"
    try:
        ptos = requests.get(query, params, headers = HEADERS).json()["items"]
    except KeyError:
        raise KeyExpiredError()
    while len(ptos) > 0:
        for pto in ptos:
            pto = pto["track"]
            artists = pto["artists"]
            songs_artists = []
            for artist in artists:
                artist_object = Artist(artist["id"], artist["name"])
                ARTISTS.add(artist_object)
                songs_artists.append(artist_object)
            tracks.append(Track(songs_artists, pto["explicit"], pto["id"], pto["name"]))
        page += 1
        params = {"limit": 50, "offset": page*50}
        try:
            ptos = requests.get(query, params, headers = HEADERS).json()["items"]
        except KeyError:
            raise KeyExpiredError()
    return tracks

def get_album_tracks(album_id: str) -> [Track]:
    tracks = []
    query = "https://api.spotify.com/v1/albums/{}/tracks".format(album_id)
    params = {"limit": 50}
    try:
        tos = requests.get(query, params, headers = HEADERS).json()["items"]
    except KeyError:
        raise KeyExpiredError()
    for to in tos:
        artists = to["artists"]
        songs_artists = []
        for artist in artists:
            artist_object = Artist(artist["id"], artist["name"])
            ARTISTS.add(artist_object)
            songs_artists.append(artist_object)
        tracks.append(Track(songs_artists, to["explicit"], to["id"], to["name"]))
    return tracks

def get_artist_album_ids(artist_id: str) -> [str]:
    albums = []
    query = "https://api.spotify.com/v1/artists/{}/albums".format(artist_id)
    page = 0
    params = {"limit": 50, "offset": 50*page}
    try:
        aos = requests.get(query, params, headers = HEADERS).json()["items"]
    except KeyError:
        raise KeyExpiredError()
    while len(aos) > 0:
        for ao in aos:
            albums.append(ao["id"])
        page += 1
        params = {"limit": 50, "offset": 50*page}
        try:
            aos = requests.get(query, params, headers = HEADERS).json()["items"]
        except KeyError:
            raise KeyExpiredError()
    return albums

def get_tracks_from_albums_with_certain_artist(album_ids: [str], artist_id) -> [Track]:
    tracks = []
    query = "https://api.spotify.com/v1/albums"
    while len(album_ids) > 0:
        id_strings = ""
        for i in range(min(20, len(album_ids))):
            id_strings += album_ids[i] + ","
        id_strings = id_strings[:-1]
        album_ids = album_ids[20:]
        params = {"ids": id_strings}
        try:
            aos = requests.get(query, params, headers = HEADERS).json()["albums"]
        except KeyError:
            raise KeyExpiredError()
        for album in aos:
            for track in album["tracks"]["items"]:
                artists = track["artists"]
                songs_artists = []
                to_be_added = False
                for artist in artists:
                    if artist["id"] == artist_id: to_be_added = True
                    artist_object = Artist(artist["id"], artist["name"])
                    ARTISTS.add(artist_object)
                    songs_artists.append(artist_object)
                if to_be_added:
                    tracks.append(Track(songs_artists, track["explicit"], track["id"], track["name"]))
    return tracks

def get_all_tracks_from_artist(artist_id: str):
    return get_tracks_from_albums_with_certain_artist(get_artist_album_ids(artist_id), artist_id)

if __name__ == "__main__":
    tracks = get_all_tracks_from_artist(input())
    for track in tracks:
        print(track.name)
