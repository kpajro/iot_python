import paho.mqtt.client as mqtt
import json
import random
import time

def on_publish(client, userdata, mid, reason_code, properties):
    print("Message publié")

# Générer 4 nombres aléatoires
random_numbers = [random.randint(1, 100) for _ in range(4)]
payload = json.dumps({"values": random_numbers})

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_publish = on_publish
client.connect("51.38.185.58", 1883, 60)

# Publier sur le topic ingestion_abc
client.loop_start()
client.publish("ingestion_abc", payload)
client.loop_stop()
client.disconnect()
