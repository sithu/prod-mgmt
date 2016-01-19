import time
import json

class MachineState(object):
	def __init__(self) :
		self.MACHINE_FAILURE = 'MACHINE_FAILURE'
	

class ShiftState(object):
	def __init__(self):
		self.SHIFT_START = 'SHIFT_START'
		self.SHIFT_END = 'SHIFT_END'

class TaskState(object):
	def __init__(self):
		self.TASK_START = 'TASK_START'
		self.TASK_END = 'TASK_END'

class Event(object):
    
    def __init__(self, machine_id, order_id):
    	self.event = ShiftState().SHIFT_END
        self.machine_id = machine_id
        self.order_id = order_id
        self.time = time.time()

    def __str__(self):
        return self.to_JSON()
    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
