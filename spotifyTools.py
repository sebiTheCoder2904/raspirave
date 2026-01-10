import spotipy
from spotipy.oauth2 import SpotifyOAuth
import zmq
from time import sleep

scope = (
        "user-library-read ",
        "user-read-playback-state ",
        "user-modify-playback-state ",
        "user-read-currently-playing ",
        "app-remote-control ",
        "streaming ",
        "playlist-read-private ",
        "playlist-read-collaborative ",
        "playlist-modify-private ",
        "playlist-modify-public ",
        "user-read-playback-position ",
        "user-top-read ",
        "user-read-recently-played "
        )

topic2function = {
    "/spotipy/playback/next": "next_track",
    "/spotipy/playback/previous": "previous_track",
    "/spotipy/playback/toggle": "toggle_playback",
    "/spotipy/playback/current": "get_current_playback",
    "/spotipy/playback/current_pretty": "get_pretty_current_playback",
    "/spotipy/playback/trackname": "get_current_playback_trackname",
    "/spotipy/playback/artistname": "get_current_playback_artistname",
    "/spotipy/scope/get": "give_scope",
    "/spotipy/volume/set": "set_volume",
    "/spotipy/playback/total_duration": "get_current_track_duration",
    "/spotipy/playback/progress": "get_current_track_progress",
    }

class SpotifyTool:

    def __init__(self):
        self.socket = "ipc:///tmp/bus"
        self.topic_kill = "spotipy/kill"
        self.topic_playback = "spotipy/playback/state"
        self.topic_playback_update = "spotipy/playback/state/update"
        self.topic_track = "spotipy/playback/track"
        self.topic_artist = "spotipy/playback/artist"

        self.scope = scope
        self.topic2function = topic2function
        self.auth_manager = SpotifyOAuth(scope=self.scope, open_browser=False)
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)


    def get_current_playback(self):
        return self.sp.current_playback()
    
    def get_pretty_current_playback(self):
        playback = self.get_current_playback()
        if playback is None:
            return "No playback information available."
        
        item = playback.get('item', {})
        if not item:
            return "No track is currently playing."
        
        artists = ', '.join(artist['name'] for artist in item.get('artists', []))
        track_name = item.get('name', 'Unknown Track')
        is_playing = playback.get('is_playing', False)
        progress_ms = playback.get('progress_ms', 0)
        duration_ms = item.get('duration_ms', 0)

        progress_min, progress_sec = divmod(progress_ms // 1000, 60)
        duration_min, duration_sec = divmod(duration_ms // 1000, 60)

        status = "Playing" if is_playing else "Paused"

        return (f"{status}: '{track_name}' by {artists} "
                f"[{progress_min}:{progress_sec:02d} / {duration_min}:{duration_sec:02d}]")

    def get_current_playback_trackname(self):
        playback = self.get_current_playback()
        if playback is None:
            return None
        
        item = playback.get('item', {})
        if not item:
            return None
        
        return item.get('name', None)

    def get_current_playback_artistname(self):
        playback = self.get_current_playback()
        if playback is None:
            return None
        
        item = playback.get('item', {})
        if not item:
            return None
        
        artists = item.get('artists', [])
        if not artists:
            return None
        
        return artists[0].get('name', None)

    def give_scope(self):
        return self.scope

    def next_track(self):
        self.sp.next_track()

    def previous_track(self):
        self.sp.previous_track()
    
    def toggle_playback(self):
        playback = self.get_current_playback()
        if playback is None:
            print("No playback information available.")
            return
        
        is_playing = playback.get('is_playing', False)
        if is_playing:
            self.sp.pause_playback()
        else:
            self.sp.start_playback()

    def set_volume(self, volume_percent):
        if 0 <= volume_percent <= 100:
            self.sp.volume(volume_percent)
        else:
            print("Volume percent must be between 0 and 100.")

    def get_current_track_duration(self):
        playback = self.get_current_playback()
        if playback is None:
            return 0
        
        item = playback.get('item', {})
        if not item:
            return 0
        
        return item.get('duration_ms', 0)

    def get_current_track_progress(self):
        playback = self.get_current_playback()
        if playback is None:
            return 0
        
        return playback.get('progress_ms', 0)


    def printEnvVars(self):
        import os
        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        print(f"Client ID: {client_id}")
        print(f"Client Secret: {client_secret}")


    def zmq_manager_thread(self):
        from zmqTool import ZmqTool
        zmq_tool = ZmqTool()

        # while True:
        #     if zmq_tool.listen_message(self.topic_playback) == "update":
        #         playback = self.get_pretty_current_playback()
        #         zmq_tool.publish_message(self.topic_playback, playback)
        while True:
            for topic, function_name in topic2function.items():
                if zmq_tool.listen_message(topic) == "update":
                    function = getattr(self, function_name, None)
                    if function:
                        result = function()
                        zmq_tool.publish_message(topic, str(result))

            sleep(1)

            

