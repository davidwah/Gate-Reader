import paho.mqtt.client as mqtt
from setorDB import setor_Data


### Koneksi MQTT ###
MQTT_Broker = "localhost"
MQTT_Port   = 1883
Keep_Alive_Interval = 60
MQTT_Topic  = "parkir/#"

def on_connect(self, mosq, obj, rc):
    self.subscribe(MQTT_Topic, 0)
    print("Connected with result code " + str(rc))

def on_message(mosq, obj, msg):
    print "MQTT Data diterima . . ."
    print "MQTT Topic: " + msg.topic
    print "Data: " + msg.payload
    print " "
    setor_Data(msg.topic, msg.payload)

def on_subcribe(mosq, obj, mid, grandted_qos):
    pass

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subcribe
mqttc.connect(MQTT_Broker, MQTT_Port, Keep_Alive_Interval)

def publish_topic(topic, message):
    mqttc.publish(topic, message)
    print("Terkirim: " + str(message) + " " + "on MQTT Topic: " + str(topic))
    print " "


mqttc.loop_forever()
