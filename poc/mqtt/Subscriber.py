import paho.mqtt.client as paho
 
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
 
def on_message(client, userdata, msg):
    print("topic:" +msg.topic+" qos:"+str(msg.qos)+" msg:"+str(msg.payload))    
 
client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect("localhost", 3000)
client.subscribe("time", qos=1)
 
#client.loop_start()
client.loop_forever()