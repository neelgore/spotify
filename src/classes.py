from collections import namedtuple

Track = namedtuple("Track", ["artists", "explicit", "id", "name"])
Album = namedtuple("Album", ["album_type", "id", "name", "tracks"])
Artist = namedtuple("Artist", ["id", "name"])
BaconArtist = namedtuple("BaconArtist", ["artist", "depth", "songlist"])
