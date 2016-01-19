import paho.mqtt.client as paho
import time
import event

def on_publish(client, userdata, mid):
    print("msg_id: "+str(mid))
 
client = paho.Client()
client.on_publish = on_publish
client.connect("localhost", 3000)
client.loop_start()
 
while True:
    print 'Select event:'
    print '1. Machine Failure'
    print '2. SHIFT End'
    print '3. Task End'
    i = input()
    eventObj = event.Event(1, 1)

    if i == 1:
        eventObj.event = event.MachineState().MACHINE_FAILURE
    elif i == 2:
        eventObj.event = event.ShiftState().SHIFT_END
    elif i == 3:
        eventObj.event = event.TaskState().TASK_END

    (rc, mid) = client.publish("event", str(eventObj.__str__()), qos=1)
    time.sleep(3)