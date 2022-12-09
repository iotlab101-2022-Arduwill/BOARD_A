import sys
import paho.mqtt.client as mqtt

topic= "id/jongminkim/sensor/evt/#"
# server = "54.156.77.237" # mine
server = "54.147.58.115"


def on_connect(client, userdata, flags, rc):
    print("Connected with RC : " + str(rc))
    client.subscribe(topic)
    client.subscribe("modeSelection")

global EV
EV = 0
def on_message(client, userdata, msg):
    # print("act")
    global EV
    if(msg.topic == "modeSelection"):

        if(msg.topic.split('/')[4] == 'encoderValue'):
            encoder = int(msg.payload.decode('utf-8'))
            EV = encoder
            
        if(msg.topic.split('/')[4] == 'temperature'):
            temperature = float(msg.payload.decode('utf-8'))
            if temperature >= EV:
                client.publish("id/jongminkim/relay/cmd", "on")
                
            else:
                client.publish("id/jongminkim/relay/cmd", "off")
            
        elif(msg.topic.split('/')[4] == 'humidity'):
            pass

        elif(msg.topic.split('/')[4] == 'light'):
            light = int(msg.payload.decode('utf-8'))
            if light <= 200:
                client.publish("id/jongminkim/light/cmd", "on")
                # print(light)
            else:
                client.publish("id/jongminkim/light/cmd", "off")
    


client = mqtt.Client()
client.connect(server, 1883, 60)
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
