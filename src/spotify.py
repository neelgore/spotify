import requests
import api_requests
from classes import Track, Artist, BaconArtist
from queue import Queue
from time import sleep


def get_all_tracks_from_artist(artist_id: str) -> [Track]:
    return api_requests.get_tracks_from_albums_with_certain_artist(api_requests.get_artist_album_ids(artist_id), artist_id)

def artists_from_tracklist(tracklist: [Track], to_be_skipped) -> dict:
    artists = {}
    for track in tracklist:
        for a in track.artists:
            if a not in to_be_skipped:
                artists[a] = track
    return artists

def next_set_of_artists(current: Artist, to_be_skipped):
    return artists_from_tracklist(get_all_tracks_from_artist(current.artist.id), to_be_skipped)

def bacon_number(start: Artist, end: Artist, max_depth: int) -> BaconArtist:
    if start == end: return BaconArtist(end, 0, [])
    to_be_skipped = {start}
    queue = Queue()
    queue.put(BaconArtist(start, 0, []))
    current = queue.get()
    node_count = 1
    print("\nRunning . . .\n")
    for n in range(max_depth):
        print("depth: ", n + 1)
        while current.depth == n:
            horizon = next_set_of_artists(current, to_be_skipped)
            for artist in horizon:
                if artist == end:
                    return BaconArtist(artist, n + 1, current.songlist + [horizon[artist]])
                to_be_skipped.add(artist)
                queue.put(BaconArtist(artist, n + 1, current.songlist + [horizon[artist]]))
                node_count += 1
                print(node_count)
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
    print_baconartist(bacon_number(api_requests.search_for_artist(), api_requests.search_for_artist(), 10))
