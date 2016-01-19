import paho.mqtt.client as paho
import json

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
 
def on_message(client, userdata, msg):
    print("topic:" +msg.topic+" qos:"+str(msg.qos)+" msg:"+str(msg.payload))    
    event = json.loads(msg.payload)
    print event['event']

    if event['event'] == 'SHIFT_END':
    	print 'SHIFT_END_ROUTINE'

    elif event['event'] == 'TASK_END':
    	print 'TASK_END_ROUTINE'

    elif event['event'] == 'MACHINE_FAILURE':
    	print 'MACHINE_FAILURE_ROUTINE'
 
client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect("localhost", 3000)
client.subscribe("event", qos=1)
 
#client.loop_start()
client.loop_forever()