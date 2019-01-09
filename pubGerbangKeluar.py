import paho.mqtt.client as mqtt
from datetime import datetime
import json, threading, random
import zbar
from sys import argv



### Fungsi dari Zbar ###
proc = zbar.Processor()
proc.parse_config('enable')
device = '/dev/video0'		#sesuaikan dengan port device
if len(argv) > 1:
    	device =argv[1]
proc.init(device)


#### Koneksi MQTT ####
MQTT_Broker = "192.168.1.102"
MQTT_Port = 1883
Keep_Alive_Interval = 45

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


### Kirim data MQTT sesuai dengan Topik (GerbangKeluar)
def publish_To_Topic(topic, message):
	mqttc.publish(topic,message)
	print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
	print ""

    
def kirim_data_MQTT(proc, image, closure):
    for symbol in image.symbols:
   		print 'decode', symbol.type, 'symbol', '%s' % symbol.data
   		# data_keluarInput = str(symbol.data) 
   		data_keluarInput = re.findall(r'^\w+|\w+$', symbol.data) 
   		data_Keluar = {}
   		data_Keluar['data_Keluar'] = data_keluarInput
   		data_json_keluar = json.dumps(data_Keluar)

	   	print "Data keluar yang terkirim: "+ str(data_keluarInput)
   		publish_To_Topic (MQTT_Topic_GerbangKeluar, data_json_keluar)
		publish_To_Topic (MQTT_Topic_palangKeluar, 1)

proc.set_data_handler(kirim_data_MQTT)
proc.visible = True
proc.active = True

try:
	# tetap jalankan proses scan QR_Code sampai terima input
    proc.user_wait()
except zbar.WindowClosed, e:
	pass
