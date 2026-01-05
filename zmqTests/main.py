from time import sleep
import zmq


topic = "spotipy/playback/state"

sub = zmq.Context().socket(zmq.SUB)
sub.connect("ipc:///tmp/bus")
sub.setsockopt_string(zmq.SUBSCRIBE, topic)

sleep(0.1)

while True:
    topic, msg = sub.recv_string().split(" ", 1)
    print("Received:", msg)



