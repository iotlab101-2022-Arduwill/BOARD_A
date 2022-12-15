import sys
import datetime
import paho.mqtt.client as mqtt
from influxdb import client as influxdb
db = influxdb.InfluxDBClient('54.147.58.115', 8086, 'iot', 'iot', 'mydb')

# topic= "id/jongminkim/sensor/evt/#"

# server = "54.156.77.237" # mine
server = "54.147.58.115"


def on_connect(client, userdata, flags, rc):
    print("Connected with RC : " + str(rc))
    client.subscribe("id/jongminkim/sensor/evt/#")
    client.subscribe("id/jihoon/sensor/evt/#")
    client.subscribe("id/jongminkim//sensor/evt/modeSelection")
    client.subscribe("id/jihoon/sensor/evt/modeSelection")
    client.subscribe("takepicture")

# global EV
# global MODE_SELECT
JM_EV = 0
JH_EV = 0
MODE_JM_MODE = 0
MODE_JH_MODE = 0

def on_message(client, userdata, msg):
    # print("act")
    global JM_EV
    global JH_EV
    global MODE_JM_MODE
    global MODE_JH_MODE
    if(msg.topic == "id/jongminkim/sensor/evt/modeSelection"):
        mode_jm = int(msg.payload.decode('utf-8'))
        MODE_JM_MODE = mode_jm
        print("MODE_JM_MODE: ", MODE_JM_MODE)

    if MODE_JM_MODE == 1:
        if(msg.topic.split('/')[4] == 'encoderValue' and msg.topic.split('/')[1] == 'jongminkim'):
            encoderV = int(msg.payload.decode('utf-8'))
            JM_EV = encoderV
            # db.write_points([{'measurement':"cpu", 'tags':{"host":"jongminkim", "region":"us-north"}, 'fields':{'encoder':EV}}])
            print("JM_EV:", JM_EV)
        
        elif(msg.topic.split('/')[4] == 'temperature' and msg.topic.split('/')[1] == 'jongminkim'):
            temperature = float(msg.payload.decode('utf-8'))
            if temperature >= JM_EV:
                client.publish("id/jongminkim/relay/cmd", "on")
                
            else:
                client.publish("id/jongminkim/relay/cmd", "off")

            # db.write_points([{'measurement':"cpu", 'tags':{"host":"jongminkim", "region":"us-north"}, 'fields':{'temperature':temperature}}])
            # result = db.query('select temperature from cpu where time > now() - 1m')
            # print(result)

        elif(msg.topic.split('/')[4] == 'humidity'and msg.topic.split('/')[1] == 'jongminkim'):
            humidity = float(msg.payload.decode('utf-8'))
            # db.write_points([{'measurement':"cpu", 'tags':{"host":"jongminkim", "region":"us-north"}, 'fields':{'humidity':humidity}}])


        elif(msg.topic.split('/')[4] == 'light' and msg.topic.split('/')[1] == 'jongminkim'):
            light = int(msg.payload.decode('utf-8'))
            if light <= 200:
                client.publish("id/jongminkim/light/cmd", "on")
                # print(light)
            else:
                client.publish("id/jongminkim/light/cmd", "off")
            # db.write_points([{'measurement':"cpu", 'tags':{"host":"jongminkim", "region":"us-north"}, 'fields':{'light':light}}])
########################################
    if(msg.topic == "id/jihoon/sensor/evt/modeSelection"):
        mode_jh = int(msg.payload.decode('utf-8'))
        MODE_JH_MODE = mode_jh
        print("MODE_JH_MODE: ", MODE_JH_MODE)

    if MODE_JH_MODE == 1:
        if(msg.topic.split('/')[4] == 'encoderValue' and msg.topic.split('/')[1] == 'jihoon'):
            jh_encoder = int(msg.payload.decode('utf-8'))
            JH_EV = jh_encoder
            # db.write_points([{'measurement':"cpu", 'tags':{"host":"jihoon", "region":"us-north"}, 'fields':{'encoder':EV}}])
        
        elif(msg.topic.split('/')[4] == 'temperature' and msg.topic.split('/')[1] == 'jihoon'):
            jh_temperature = float(msg.payload.decode('utf-8'))
            if jh_temperature >= JH_EV:
                client.publish("id/jihoon/relay/cmd", "on")
                
            else:
                client.publish("id/jihoon/relay/cmd", "off")

            # db.write_points([{'measurement':"cpu", 'tags':{"host":"jihoon", "region":"us-north"}, 'fields':{'temperature':jh_temperature}}])
            # result = db.query('select temperature from cpu where time > now() - 1m')
            # print(result)

        elif(msg.topic.split('/')[4] == 'humidity' and msg.topic.split('/')[1] == 'jihoon'):
            jh_humidity = float(msg.payload.decode('utf-8'))
            # db.write_points([{'measurement':"cpu", 'tags':{"host":"jihoon", "region":"us-north"}, 'fields':{'humidity':jh_humidity}}])


        elif(msg.topic.split('/')[4] == 'light' and msg.topic.split('/')[1] == 'jihoon'):
            jh_light = int(msg.payload.decode('utf-8'))
            if jh_light <= 200:
                client.publish("id/jihoon/light/cmd", "on")
                # print(light)
            else:
                client.publish("id/jihoon/light/cmd", "off")
            # db.write_points([{'measurement':"cpu", 'tags':{"host":"jihoon", "region":"us-north"}, 'fields':{'light':jh_light}}])
        
    # 자동모드 일 때 카메라 동작
    elif(msg.topic.split('/')[4] == 'distance' and msg.topic.split('/')[1] == 'jihoon'):
            jh_distance = float(msg.payload.decode('utf-8'))
            if jh_distance <= 15:
                print("15cm 이하")
                client.publish("cctv")
            # db.write_points([{'measurement':"cpu", 'tags':{"host":"jihoon", "region":"us-north"}, 'fields':{'light':jh_light}}])

    if (msg.topic == "id/jihoon/sensor/evt/takepicture"):
        
        date = str(datetime.datetime.now())
        date = date[:19].replace(":", '_') 
        date = date.replace(' ', '_')
        # date = date.strftime('%YY_%mm_%DD_%HH_%MM_%SS')
        print(type(date))

        f = open(date[:20]+ ".jpg", "wb")
        f.write(msg.payload)
        print("Image Received")
        f.close()   


client = mqtt.Client()
client.connect(server, 1883, 60)
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
