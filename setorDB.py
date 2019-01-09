import mysql.connector
import json
import paho.mqtt.client as mqtt


#### Koneksi MQTT ####
MQTT_Broker =  "localhost"
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

def publish_To_Topic(topic, message):
    	mqttc.publish(topic,message)
	print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
	print ""

#######################################
### Fungsi untuk kirim ke database
#######################################

### Gerbang Masuk ###
def MQTT_Topic_GerbangMasuk(jsonData):
    json_Dict = json.loads(jsonData)
    username = json_Dict['data_Masuk']
    #Koneksi dan kirim data ke Database
    connection = mysql.connector.connect(host='localhost',
                             database='myDB',
                             user='david',
                             password='admin')
    mycursor = connection.cursor(True)
    sql_up = "SELECT * from users where users.username='%s'" % username
    mycursor.execute(sql_up)
    coba = mycursor.fetchall()

    for row in coba:
        if username == username:
            print"Data User Tersedia"
            sql = "INSERT into gerbangMasuk (username) values ('%s')" % username
            sql2 = "INSERT into gorengan (pesan) values ('%s')" % username
            mycursor.execute(sql)
            mycursor.execute(sql2)
            connection.commit()
            publish_To_Topic (MQTT_Topic_palangMasuk, 1)
        elif masuk != coba:
            print "Data Tidak Ada"

### Gerbang Keluar ###
def MQTT_Topic_GerbangKeluar(jsonData):
    json_Dict = json.loads(jsonData)
    keluar = json_Dict['data_Keluar']
    #Koneksi dan kirim data ke Database
    connection = mysql.connector.connect(host='localhost',
                             database='myDB',
                             user='david',
                             password='admin')
    mycursor = connection.cursor(True)
    sql_up = "SELECT * from gerbangMasuk where username='%s'" % keluar
    mycursor.execute(sql_up)
    coba = mycursor.fetchall()

    for row in coba:
        if keluar == keluar:
            print"Data User Tersedia"
            sql = "INSERT into gerbangKeluar (username) values ('%s')" % keluar
            sql2 = "INSERT into gorengan (pesan) values ('%s')" % keluar
            mycursor.execute(sql)
            mycursor.execute(sql2)
            connection.commit()
            publish_To_Topic (MQTT_Topic_palangKeluar, 1)
        elif masuk != coba:
            print"Data Tidak Ada"


def setor_Data(Topic, jsonData):
    if Topic == "parkir/pintuMasuk":
        #Parkir_GerbangMasuk(jsonData)
        MQTT_Topic_GerbangMasuk(jsonData)
    elif Topic == "parkir/pintuKeluar":
        #Parkir_GerbangKeluar(jsonData)
        MQTT_Topic_GerbangKeluar(jsonData)

