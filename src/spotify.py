import requests
from classes import Track, Artist, Album, BaconArtist
from queue import Queue

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
        aos = requests.get(query, params, headers = HEADERS).json()
        print(aos.keys())
        raise KeyExpiredError()
    while len(aos) > 0:
        for ao in aos:
            albums.append(ao["id"])
        page += 1
        params = {"limit": 50, "offset": 50*page}
        try:
            aos = requests.get(query, params, headers = HEADERS).json()["items"]
        except KeyError:
            aos = requests.get(query, params, headers = HEADERS).json()
            print(aos)
            raise KeyExpiredError()
    return albums

def get_tracks_from_albums_with_certain_artist(album_ids: [str], artist_id: str) -> [Track]:
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
            aos = requests.get(query, params, headers = HEADERS).json()
            print(aos)
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

def get_all_tracks_from_artist(artist_id: str) -> [Track]:
    return get_tracks_from_albums_with_certain_artist(get_artist_album_ids(artist_id), artist_id)

def search_for_artist() -> Artist:
    query = "https://api.spotify.com/v1/search"
    params = {"q": input("Enter an artist:\n"), "type": "artist", "limit": 1}
    try:
        search_results = requests.get(query, params, headers = HEADERS).json()["artists"]["items"]
    except KeyError:
            raise KeyExpiredError()
    return Artist(search_results[0]["id"], search_results[0]["name"])

def artists_from_tracklist(tracklist: [Track], to_be_skipped) -> dict:
    artists = {}
    for track in tracklist:
        for a in track.artists:
            if a not in to_be_skipped:
                artists[a] = track
    return artists

def bacon_number(start: Artist, end: Artist, max_depth: int) -> BaconArtist:
    if start == end: return BaconArtist(end, 0, [])
    to_be_skipped = {start}
    queue = Queue()
    queue.put(BaconArtist(start, 0, []))
    current = queue.get()
    print("\nRunning . . .\n")
    for n in range(max_depth):
        while current.depth == n:
            horizon = artists_from_tracklist(get_all_tracks_from_artist(current.artist.id), to_be_skipped)
            for artist in horizon:
                if artist == end:
                    return BaconArtist(artist, n + 1, current.songlist + [horizon[artist]])
                to_be_skipped.add(artist)
                queue.put(BaconArtist(artist, n + 1, current.songlist + [horizon[artist]]))
            current = queue.get()

def print_baconartist(bacon_artist: BaconArtist) -> ([Track], int):
    print("Bacon Number:", bacon_artist.depth)
    print("\nTrack list:\n")
    for track in bacon_artist.songlist:
        print(track.name)
        print("\t", end = "")
        for i in range(len(track.artists) - 1):
            print(track.artists[i].name, end = "\n\t")
        print(track.artists[-1].name)
        print()

if __name__ == "__main__":
    print_baconartist(bacon_number(search_for_artist(), search_for_artist(), 10))
