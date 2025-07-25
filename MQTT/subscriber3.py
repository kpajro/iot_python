import paho.mqtt.client as mqtt
import mysql.connector
import json
import random
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
        sensor_id = topic_parts[1]
        sensor_type = topic_parts[2]
        valeur = float(msg.payload.decode())

        cursor.execute("SELECT * FROM sensors WHERE sensor_id=%s", (sensor_id,))
        if cursor.fetchone() is None:
            # position + randomisation autour de la tour montparnasse
            base_lat = 48.8422
            base_lon = 2.3215
            rand_lat = base_lat + random.uniform(-0.002, 0.002)
            rand_lon = base_lon + random.uniform(-0.002, 0.002)

            cursor.execute(
                "INSERT INTO sensors (sensor_id, type, longitude, latitude) VALUES (%s, %s, %s, %s)",
                (sensor_id, sensor_type, rand_lat, rand_lon)
            )

        cursor.execute(
            "INSERT INTO sensor_readings (sensor_id, type, valeur) VALUES (%s, %s, %s)",
            (sensor_id, sensor_type, valeur)
        )
        db.commit()
    except Exception as e:
        print("Erreur :", e)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.mqttdashboard.com", 1883, 60)
client.loop_forever()