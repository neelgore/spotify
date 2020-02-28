import requests
import api_requests
from classes import Track, Artist, BaconArtist
from queue import Queue
from collections import namedtuple


def get_all_tracks_from_artist(artist_id: str) -> [Track]:
    return api_requests.get_tracks_from_albums_with_certain_artist(api_requests.get_artist_album_ids(artist_id), artist_id)

def artists_from_tracklist(tracklist: [Track], to_be_skipped, current: Artist) -> dict:
    artists = {}
    for track in tracklist:
        for a in track.artists:
            if a not in to_be_skipped:
                artists[a] = (track, current)
            to_be_skipped.add(a)
    return artists

def next_set_of_artists(current: Artist, to_be_skipped):
    return artists_from_tracklist(get_all_tracks_from_artist(current.artist.id), to_be_skipped, current)

def bacon_number(start: Artist, end: Artist, max_depth: int) -> BaconArtist:
    if start == end: return BaconArtist(end, 0, [], [])
    to_be_skipped = {start}
    queue = Queue()
    queue.put(BaconArtist(start, 0, [], []))
    current = queue.get()
    print("\nRunning . . .\n")
    for n in range(max_depth):
        print("current depth: ", n + 1)
        while current.depth == n:
            horizon = next_set_of_artists(current, to_be_skipped)
            if len(horizon) == 0: return BaconArtist(end, -1, [], [BaconArtist(start, 0, [], [])])
            for artist in horizon:
                if artist == end:
                    return BaconArtist(artist, n + 1, current.songlist + [horizon[artist][0]], current.artistlist + [horizon[artist][1]])
                queue.put(BaconArtist(artist, n + 1, current.songlist + [horizon[artist][0]], current.artistlist + [horizon[artist][1]]))
            current = queue.get()

def print_baconartist(bacon_artist: BaconArtist) -> ([Track], int):
    print("\nResults from {} to {}:\n".format(bacon_artist.artistlist[0].artist.name, bacon_artist.artist.name))
    if bacon_artist.depth == -1:
        print("There is no connection between {} and {}.".format(bacon_artist.artistlist[0].artist.name, bacon_artist.artist.name))
        return
    print("Bacon Number:", bacon_artist.depth)
    print("\nTrack list:\n")
    for i in range(len(bacon_artist.songlist) - 1):
        print_track(bacon_artist.songlist[i], bacon_artist.artistlist[i + 1].artist)
    print_track(bacon_artist.songlist[-1], bacon_artist.artist)

def print_track(track: Track, artist_to_highlight: Artist) -> None:
    print(track.name)
    print("\t", end = "")
    for i in range(len(track.artists) - 1):
        if (track.artists[i].id == artist_to_highlight.id):
            print("> " + track.artists[i].name, end = "\n\t")
        else:
            print(track.artists[i].name, end = "\n\t")
    if track.artists[-1].id == artist_to_highlight.id:
        print("> " + track.artists[-1].name, end = "\n\t")
    else:
        print(track.artists[-1].name, end = "\n\t")
    print()

def search_and_select_artist(results = 20) -> Artist:
    artists = api_requests.search_for_artist(results)
    if len(artists) == 1:
        return artists[0]
    print()
    for i in range(len(artists)):
        print(str(i + 1) + ". " + artists[i].name)
    print()
    selection = int(input("Type a number to select an artist:\n"))
    return artists[selection - 1]

if __name__ == "__main__":
    print_baconartist(bacon_number(search_and_select_artist(), search_and_select_artist(), 10))
