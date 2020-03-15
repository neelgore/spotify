import requests
import api_requests
from classes import Track, Artist, BaconArtist
from queue import Queue

def get_all_tracks_from_artist(artist: Artist) -> [Track]:
    return api_requests.get_tracks_from_albums_with_certain_artist(api_requests.get_artist_album_ids(artist.id), artist.id)

def artists_from_tracklist(tracklist: [Track], to_be_skipped, current: Artist) -> dict:
    artists = {}
    for track in tracklist:
        for a in track.artists:
            if a not in to_be_skipped:
                artists[a] = (track, current)
            to_be_skipped.add(a)
    return artists

def next_set_of_artists(current: BaconArtist, to_be_skipped) -> dict:
    return artists_from_tracklist(get_all_tracks_from_artist(current.artist), to_be_skipped, current)

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
            for artist in horizon:
                if artist == end:
                    return BaconArtist(artist, n + 1, current.songlist + [horizon[artist][0]], current.artistlist + [horizon[artist][1]])
                queue.put(BaconArtist(artist, n + 1, current.songlist + [horizon[artist][0]], current.artistlist + [horizon[artist][1]]))
            if queue.empty(): return BaconArtist(end, -1, [], [BaconArtist(start, 0, [], [])])
            current = queue.get()
    return BaconArtist(end, -2, max_depth, [BaconArtist(start, 0, [], [])])

def print_baconartist(bacon_artist: BaconArtist) -> ([Track], int):
    print("\nResults from {} to {}:\n".format(bacon_artist.artistlist[0].artist.name, bacon_artist.artist.name))
    if bacon_artist.depth == -1:
        print("There is no connection between {} and {}.".format(bacon_artist.artistlist[0].artist.name, bacon_artist.artist.name))
        return
    if bacon_artist.depth == -2:
        print("There is no connection between {} and {} with max depth {}.".format(bacon_artist.artistlist[0].artist.name, bacon_artist.artist.name, bacon_artist.songlist))
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
        if (artist_to_highlight is not None and track.artists[i].id == artist_to_highlight.id):
            print("> " + track.artists[i].name, end = "\n\t")
        else:
            print(track.artists[i].name, end = "\n\t")
    if artist_to_highlight is not None and track.artists[-1].id == artist_to_highlight.id:
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

def same_contents_in_list(artist_list1: [Artist], artist_list2: [Artist]) -> bool:
    if len(artist_list1) != len(artist_list2): return False
    artist_set1 = set()
    for artist in artist_list1:
        artist_set1.add(artist.id)
    for artist in artist_list2:
        if artist.id not in artist_set1:
            return False
    return True

def same_title(title1: str, title2: str) -> bool:
    return title1 in title2 or title2 in title1

def title_or_similar_in_dict(title: str, dictionary: dict) -> (bool, str, [Artist]):
    for string in dictionary.keys():
        if same_title(title, string): return (True, min(title, string, key = len), dictionary[string])
    return (False, None, None)

