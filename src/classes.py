from collections import namedtuple

Track = namedtuple("Track", ["album", "artists", "explicit", "id", "name", "popularity"])
Album = namedtuple("Album", ["album_type", "id", "label", "name", "popularity", "release_date", "release_date_precision", "tracks"])
Artist = namedtuple("Artist", ["id", "name", "popularity"])
