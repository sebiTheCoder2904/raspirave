from queue import Queue
from collections import defaultdict

class Bus:
    def __init__(self):
        self.topics = defaultdict(list)

    def subscribe(self, topic):
        q = Queue()
        self.topics[topic].append(q)
        return q

    def publish(self, topic, msg):
        for q in self.topics[topic]:
            q.put(msg)


