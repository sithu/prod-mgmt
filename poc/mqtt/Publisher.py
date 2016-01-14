import paho.mqtt.client as paho
import time
import QueueTask

def on_publish(client, userdata, mid):
    print("msg_id: "+str(mid))
 
client = paho.Client()
client.on_publish = on_publish
client.connect("localhost", 3000)
client.loop_start()
 
while True:
    task = QueueTask.QueueTask(1, 1)
    (rc, mid) = client.publish("time", str(task.__str__()), qos=1)
    time.sleep(3)