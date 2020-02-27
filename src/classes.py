from collections import namedtuple

Track = namedtuple("Track", ["artists", "explicit", "id", "name"])
Artist = namedtuple("Artist", ["id", "name"])
BaconArtist = namedtuple("BaconArtist", ["artist", "depth", "songlist"])
