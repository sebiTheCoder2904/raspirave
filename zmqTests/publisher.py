import zmq
from time import sleep

topic = "spotipy/playback/state"
pub = zmq.Context().socket(zmq.PUB)
pub.bind("ipc:///tmp/bus")

sleep(0.1)


while True:
    pub.send_string(f"{topic} Playing")
    sleep(1)
    pub.send_string(f"{topic} Paused")
    sleep(1)
