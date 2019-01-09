import paho.mqtt.client as mqtt
from datetime import datetime
import json, threading, random
import zbar
import re
from sys import argv



### Fungsi dari Zbar ###
proc = zbar.Processor()
proc.parse_config('enable')
device = '/dev/video1'		#sesuaikan dengan port device
if len(argv) > 1:
    	device =argv[1]
proc.init(device)


#### Koneksi MQTT ####
MQTT_Broker = "localhost" #"192.168.1.102"
MQTT_Port = 1883
Keep_Alive_Interval = 60

MQTT_Topic_GerbangMasuk = "parkir/pintuMasuk"
MQTT_Topic_GerbangKeluar = "parkir/pintuKeluar"
MQTT_Topic_palangMasuk = "parkir/palangMasuk"
MQTT_Topic_palangKeluar = "parkir/palangKeluar"


####
def on_connect(client, userdata, rc):
    	if rc != 0:
		pass
		print "Gagal terhubung dengan MQTT Broker..."
	else:
		print "Terhubung dengan MQTT Broker: " + str(MQTT_Broker)

def on_publish(client, userdata, mid):
	pass

def on_disconnect(client, userdata, rc):
	if rc !=0:
		pass

mqttc = mqtt.Client()

mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish

mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))		


### Kirim data MQTT sesuai dengan Topik (GerbangMasuk)
def publish_To_Topic(topic, message):
	mqttc.publish(topic,message)
	print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
	print ""

def kirim_data_MQTT(proc, image, closure):
    for symbol in image.symbols:
   		print 'decode', symbol.type, 'symbol', '%s' % symbol.data
		data_masukInput = re.findall(r'^\w+|\w+$', symbol.data)
   		data_Masuk = {}
   		data_Masuk['data_Masuk'] = data_masukInput
   		data_json_masuk = json.dumps(data_Masuk)

	   	print "Data masuk yang terkirim: " + str(data_masukInput)
   		publish_To_Topic (MQTT_Topic_GerbangMasuk, data_json_masuk)
		# publish_To_Topic (MQTT_Topic_palangMasuk, 1)

proc.set_data_handler(kirim_data_MQTT)
proc.visible = True
proc.active = True
try:
    # tetap jalankan proses scan QR_Code sampai terima input
    proc.user_wait()
except zbar.WindowClosed, e:
	pass

