import api_requests
import spotify_tools
from classes import Track, Artist, BaconArtist


def run_bacon_artist() -> None:
    print("DISTANCE BETWEEN TWO ARTISTS\n")
    spotify_tools.print_baconartist(
        spotify_tools.bacon_number(
            spotify_tools.search_and_select_artist(),
            spotify_tools.search_and_select_artist(),
            int(input("How deep do you want to look? Enter an integer:\n"))))
    print("\n")

def run_artist_count_of_playlist() -> None:
    print("ARTIST WHO APPEARS THE MOST ON A PLAYLIST\n")
    playlist_id = input("Enter the playlist id (the numbers and letters at the end of the spotify URL):\n")
    tracks = api_requests.get_playlist_tracks(playlist_id)
    name = api_requests.get_playlist_name(playlist_id)
    artists = {}
    artist_names = []
    for track in tracks:
        for artist in track.artists:
            if artist in artists:
                artists[artist] += 1
            else:
                artists[artist] = 1
                artist_names.append(artist.name)
    sorted_artists = sorted(artists.items(), key=lambda x: x[1], reverse = True)
    print()
    print("Results for {}:\n".format(name))
    for artist in sorted_artists:
        print(artist[0].name + str(artist[1]).rjust(5 + len(max(artist_names, key = len)) - len(artist[0].name)))
    print("\n")

def run_artist_connections() -> None:
    print("ARTISTS WHO HAVE COLLABORATED WITH GIVEN ARTIST\n")
    start = spotify_tools.search_and_select_artist()
    start_set = set()
    start_set.add(start)
    connections = spotify_tools.next_set_of_artists(BaconArtist(start, 0, [], []), start_set)
    connections = sorted(connections.keys(), key = lambda x: x.name.lower())
    print()
    print("Results: {}\n".format(len(connections)))
    for artist in connections:
        print(artist.name)
    print("\n")

def run_playlist_duplicates() -> None:
    print("FIND DUPLICATES IN PLAYLIST\n")
    playlist_id = input("Enter the playlist id (the numbers and letters at the end of the spotify URL):\n")
    tracks = api_requests.get_playlist_tracks(playlist_id)
    name = api_requests.get_playlist_name(playlist_id)
    track_dict = {}
    duplicates = set()
    for track in tracks:
        tup = spotify_tools.title_or_similar_in_dict(track.name, track_dict)
        if tup[0] and spotify_tools.same_contents_in_list(tup[2], track.artists):
            duplicates.add(tup[1])
        track_dict[track.name] = track.artists
    print()
    if len(duplicates) == 0:
        print("No duplicates found")
    else:
        print("The following tracks are duplicated:\n")
        for track in duplicates:
            print(track)
    print("\n")

if __name__ == "__main__":
    run_artist_connections()
