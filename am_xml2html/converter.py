import re
import xml.etree.ElementTree as ET
from datetime import datetime

from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape

from .jinja_filters import filter_pluralize
from .jinja_filters import filter_seconds_to_mm_ss


class Xml2HtmlConverter:
    def __init__(self, xml_file_path: str, html_file_path: str) -> None:
        self._xml_file_path = xml_file_path
        self._html_file_path = html_file_path
        self._dump_info = {}
        self._tracks_data_by_artists = {}
        self._tracks_data_by_playlists = {}
        self._tracks_data_by_ids = {}
        self._html = None

    def _parse_main_items(self, root_item: ET.Element) -> None:
        key_root_item = None  # previous tag
        for main_item in root_item:
            main_item_tag = getattr(main_item, 'tag', None)
            if main_item_tag == 'key':
                key_root_item = main_item
                continue

            if getattr(key_root_item, 'text', None) == 'Tracks' and main_item.tag == 'dict':
                self._parse_tracks(main_item)
            elif getattr(key_root_item, 'text', None) == 'Playlists':
                self._parse_playlists(main_item)
            elif getattr(key_root_item, 'text', None) == 'Date':
                date_iso: str = main_item.text
                self._dump_info['created_at'] = datetime.fromisoformat(date_iso)

    def _parse_tracks(self, main_item: ET.Element) -> None:
        for track_item in main_item:
            if track_item.tag != 'dict':
                continue

            artist_name = None
            album_name = None
            track_name = None
            track_num = None
            track_id = None
            track_total_time_msecs = None
            track_year = None
            year = None
            genre = None

            key_track_line = None  # previous tag
            for track_line in track_item:
                track_line_tag = getattr(track_line, 'tag', None)
                if track_line_tag == 'key':
                    key_track_line = track_line
                    continue

                if key_track_line.text == 'Name':
                    track_name = track_line.text
                elif key_track_line.text == 'Track ID':
                    track_id = track_line.text
                elif key_track_line.text == 'Track Number':
                    track_num = track_line.text
                elif key_track_line.text == 'Artist':
                    artist_name = track_line.text
                elif key_track_line.text == 'Album':
                    album_name = track_line.text
                elif key_track_line.text == 'Total Time':
                    track_total_time_msecs = track_line.text
                elif key_track_line.text == 'Year':
                    track_year = track_line.text
                    if not year:
                        year = track_line.text
                elif key_track_line.text == 'Genre' and not genre:
                    genre = track_line.text

            if not artist_name or not album_name or not track_name or not track_num:
                continue

            artist_data = self._tracks_data_by_artists.get(artist_name) or {}
            album_data = artist_data.get(album_name) or {}

            # Add track
            track_data = dict(
                album=album_name,
                artist=artist_name,
                id=track_id,
                name=track_name,
                number=int(track_num),
                total_time=int(int(track_total_time_msecs) / 1000) if track_total_time_msecs else None,
                year=track_year,
            )

            tracks = album_data.get('tracks') or []
            tracks = sorted(tracks, key=lambda track: track['number'])
            tracks.append(track_data)

            self._tracks_data_by_ids[track_id] = track_data

            # Add album
            album_data['tracks'] = tracks

            if 'year' not in album_data:
                album_data['year'] = year

            if 'genre' not in album_data:
                album_data['genre'] = genre

            # Add artist
            artist_data[album_name] = album_data
            self._tracks_data_by_artists[artist_name] = artist_data

    def _parse_playlists(self, main_item: ET.Element) -> None:
        for playlist_item in main_item:
            playlist_name = None
            playlist_id = None
            track_ids = []

            skip_playlist = False
            key_playlist_item_line = None  # previous tag
            for playlist_item_line in playlist_item:
                playlist_item_line_tag = getattr(playlist_item_line, 'tag', None)
                if playlist_item_line_tag == 'key':
                    key_playlist_item_line = playlist_item_line
                    continue

                if key_playlist_item_line.text == 'Name':
                    playlist_name = playlist_item_line.text
                elif key_playlist_item_line.text == 'Playlist ID':
                    playlist_id = playlist_item_line.text
                elif key_playlist_item_line.text == 'Visible':
                    if playlist_item_line.tag == 'false':
                        skip_playlist = True

                if playlist_item_line.tag == 'array':
                    for track_item in playlist_item_line:
                        for track_line in track_item:
                            if track_line.tag == 'integer':
                                track_ids.append(track_line.text)

            if skip_playlist:
                continue

            if not playlist_name or not playlist_id:
                continue

            self._tracks_data_by_playlists[playlist_name] = dict(
                id=playlist_id,
                name=playlist_name,
                tracks=[self._tracks_data_by_ids.get(track_id, {}) for track_id in track_ids],
            )

    def parse_xml(self) -> None:
        tree = ET.parse(self._xml_file_path)
        root = tree.getroot()
        for root_item in root:
            self._parse_main_items(root_item)

    def generate_html(self) -> None:
        artists_data = dict(sorted(self._tracks_data_by_artists.items()))
        playlists_data = dict(sorted(self._tracks_data_by_playlists.items()))

        env = Environment(
            loader=PackageLoader('am_xml2html', package_path='templates'),
            autoescape=select_autoescape(),
        )
        env.filters['pluralize'] = filter_pluralize
        env.filters['seconds_to_mm_ss'] = filter_seconds_to_mm_ss

        template = env.get_template('index.jinja2')
        context = dict(
            info={**self._dump_info, 'generated_at': datetime.now()},
            artists=artists_data,
            playlists=playlists_data,
        )

        self._html = template.render(context).replace('\n', ' ')
        self._html = re.sub(r'\s+', ' ', self._html)

    def save_html(self) -> None:
        with open(self._html_file_path, 'w') as f:
            f.write(self._html)
