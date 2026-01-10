from spotipy.oauth2 import SpotifyOAuth
from spotifyTools import SpotifyTool
import os
from time import sleep

st = SpotifyTool()

print("Starting playback test...")

print(st.get_pretty_current_playback())

print(str(st.get_current_track_progress()) + " seconds into the track.")
print(str(st.get_current_track_duration()) + " seconds is the total duration.")

print("Artist Name: " + str(st.get_current_playback_artistname()))
print("Track Name: " + str(st.get_current_playback_trackname()))

print(st.sp.current_playback())
print("Playback test completed.")
