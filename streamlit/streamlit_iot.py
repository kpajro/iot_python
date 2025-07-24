import streamlit as st
import paho.mqtt.publish as publish
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="iot_database"
)

if st.button("Activer l'arrosage"):
    publish.single("arrosage/control", "open", hostname="broker.mqttdashboard.com")

if st.button("Désactiver l'arrosage"):
    publish.single("arrosage/control", "close", hostname="broker.mqttdashboard.com")

df = pd.read_sql("SELECT * FROM sensor_readings ORDER BY timestamp DESC", conn)

st.title("Données météo")

sensor_ids = df["sensor_id"].unique()
sensor_choice = st.selectbox("Choisissez un capteur", sensor_ids)

sensor_df = df[df["sensor_id"] == sensor_choice]

types_disponibles = sensor_df["type"].unique()
type_choice = st.selectbox("Choisissez un type de mesure", types_disponibles)

filtered_df = sensor_df[sensor_df["type"] == type_choice]

st.line_chart(filtered_df.set_index("timestamp")["value"])

st.metric("Moyenne", f"{filtered_df['value'].mean():.2f}")
st.metric("Min", f"{filtered_df['value'].min():.2f}")
st.metric("Max", f"{filtered_df['value'].max():.2f}")

conn.close()