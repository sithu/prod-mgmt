import paho.mqtt.client as paho
import time
 
def on_publish(client, userdata, mid):
    print("msg_id: "+str(mid))
 
client = paho.Client()
client.on_publish = on_publish
client.connect("localhost", 3000)
client.loop_start()
 
while True:
    temperature = time.time()
    (rc, mid) = client.publish("time", str(temperature), qos=1)
    time.sleep(3)