import zmq
from time import sleep
import json
from spotifyTools import SpotifyTool
from upsTools import UpsTools

spotipyTopics = SpotifyTool().topic2function.keys()
appTopics = {
    "/app/current": "draw_spotifyApp",
    "/app/showTopbar": "true",
    }
upsTopics = UpsTools().upsTopic.keys()

class ZmqTool:
    def __init__(self):
        self.upsTopics = upsTopics
        self.appTopics = appTopics
        self.spotipyTopics = spotipyTopics

        self.last = {k: "none" for k in spotipyTopics}
        self.last.update(appTopics)
        self.last.update({k: "none" for k in upsTopics})



        self.address = "ipc:///tmp/bus"
        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.REQ)
        self.sock.connect(self.address)
        # sleep once is fine here
        sleep(0.1)

    def publish_message(self, topic, message):
        self.sock.send_string(f"{topic} {message}")
        self.sock.recv_string()  # REQ/REP handshake

    def listen_message(self, topic):
        self.sock.send_string(f"{topic} get")
        return self.sock.recv_string()

    def get_dict_message(self):
        self.sock.send_string("hi getDict")
        return json.loads(self.sock.recv_string())


    def zmq_rep_thread(self):
        context = zmq.Context()
        rep = context.socket(zmq.REP)
        rep.bind(self.address)

        while True:
            topic, message = rep.recv_string().split(' ', 1)
            if message == "get":
                value = self.last.get(topic)
                rep.send_string(value if value is not None else "")
            elif message == "getDict":
                rep.send_string(json.dumps(self.last))
            else:
                self.last[topic] = message
                rep.send_string("ok")

            sleep(0.05)

