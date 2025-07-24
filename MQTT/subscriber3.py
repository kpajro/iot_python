import paho.mqtt.client as mqtt
import mysql.connector
import json
from datetime import datetime

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="iot_database"
)
cursor = db.cursor()

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connecté au broker")
    client.subscribe("kstest/#")

def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split("/")
        sensor_type = topic_parts[-1]
        value = float(msg.payload.decode())
        
        print(f"Recu: {sensor_type} = {value}")
        
        cursor.execute(
            "INSERT INTO sensor_readings (type, value) VALUES (%s, %s)",
            (sensor_type, value)
        )
        db.commit()
    except Exception as e:
        print("erreur au moment de l'envoi", e)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.mqttdashboard.com", 1883, 60)
client.loop_forever()