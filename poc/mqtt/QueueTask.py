import time
import json

class QueueTask(object):
    
    def __init__(self, machine_id, order_id):
        self.machine_id = machine_id
        self.order_id = order_id
        self.time = time.time()

    def __str__(self):
        return self.to_JSON()
    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
