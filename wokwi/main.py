import network
import time
from machine import Pin, ADC, PWM
import dht
import ujson
import utime, math
from umqtt.simple import MQTTClient

def lightToPercent(val):
  light = 100 - (val * 100 / 4095)
  return round(light)

def mqtt_servo_callback(topic, msg):
  topic = topic.decode()
  msg = msg.decode()
  print("Commande Servo:", msg)
  if topic == ARROSAGE_TOPIC:
    if msg == "open":
      print("Arrosage activé")
      set_servo_angle(90)
    elif msg == "close":
      print("Arrosage arreté")
      set_servo_angle(0)
    else:
        print("nothing")

def set_servo_angle(angle):
  duty = int((angle / 180) * 102 + 26)
  duty = max(-26, min(128, duty))
  print(duty)
  servo_pwm.duty(duty)

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""

ARROSAGE_TOPIC = "arrosage/control"

MQTT_TOPIC_BASE = "kstest"  # Base topic

sensor = dht.DHT22(Pin(15))
ldr = ADC(Pin(32))

servo_pwm = PWM(Pin(18), freq=50, duty=0)

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.set_callback(mqtt_servo_callback)
client.connect()
client.subscribe(ARROSAGE_TOPIC)
print("Connected!")

# Initial previous values
prev_temp = None
prev_humidity = None
prev_light = None

while True:
  print("Measuring weather conditions... ", end="")
  sensor.measure() 

  # Temperature
  temp = sensor.temperature()
  if temp != prev_temp:
    print(f"Temperature: {temp}")
    client.publish(f"{MQTT_TOPIC_BASE}/DHT22/temperature", str(temp))
    prev_temp = temp

  # Humidity
  humidity = sensor.humidity()
  if humidity != prev_humidity:
    print(f"Humidity: {humidity}")
    client.publish(f"{MQTT_TOPIC_BASE}/DHT22/humidity", str(humidity))
    prev_humidity = humidity

  # Light
  ldrval = ldr.read()
  ldr_percent = lightToPercent(ldrval)
  if ldr_percent != prev_light:
    print(f"Luminosity: {ldr_percent}")
    client.publish(f"{MQTT_TOPIC_BASE}/LDR/luminosity", str(ldr_percent))
    prev_light = ldr_percent

  client.check_msg()

  time.sleep(1)
