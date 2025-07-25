import streamlit as st
import paho.mqtt.publish as publish
import mysql.connector
import pandas as pd

arrosage_state = ["manuel", "auto"]

def get_sensors_with_location():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iot_database"
    )
    df = pd.read_sql("SELECT sensor_id, latitude, longitude FROM sensors WHERE latitude IS NOT NULL AND longitude IS NOT NULL", conn)
    conn.close()
    return df

def get_sensor_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iot_database"
    )
    df = pd.read_sql("SELECT * FROM sensor_readings ORDER BY timestamp DESC", conn)
    conn.close()
    return df

df = get_sensor_data()

st.title("Données météo")


arrosage_choice = st.selectbox("Etat d'arrosage", arrosage_state)

if arrosage_choice == "auto":
    st.subheader("Seuil d'arrosage")
    seuil_humidite = st.slider("Seuil", 0.0, 99.9, 0.0)

    st.subheader("Mode automatique activé")

    humidity_df = df[df["type"] == "humidity"]

    if not humidity_df.empty:
        moyenne = humidity_df["valeur"].mean()
        st.metric("Humidité moyenne", f"{moyenne:.2f} %")

        if moyenne < seuil_humidite:
            st.warning(f"L'humidité ({moyenne:.2f} %) est inférieure au seuil ({seuil_humidite} %). Arrosage activé.")
            publish.single("arrosage/control", "open", hostname="broker.mqttdashboard.com")
        else:
            st.success(f"L'humidité ({moyenne:.2f} %) est suffisante. Arrosage désactivé.")
            publish.single("arrosage/control", "close", hostname="broker.mqttdashboard.com")
    else:
        st.error("Aucune donnée d’humidité disponible.")

if arrosage_choice == "manuel":
    if st.button("Activer l'arrosage"):
        publish.single("arrosage/control", "open", hostname="broker.mqttdashboard.com")

    if st.button("Désactiver l'arrosage"):
        publish.single("arrosage/control", "close", hostname="broker.mqttdashboard.com")


sensor_ids = df["sensor_id"].unique()
sensor_choice = st.selectbox("Choisissez un capteur", sensor_ids)

sensor_df = df[df["sensor_id"] == sensor_choice]

types_disponibles = sensor_df["type"].unique()
type_choice = st.selectbox("Choisissez un type de mesure", types_disponibles)

filtered_df = sensor_df[sensor_df["type"] == type_choice]

st.line_chart(filtered_df.set_index("timestamp")["valeur"])

st.metric("Moyenne", f"{filtered_df['valeur'].mean():.2f}")
st.metric("Min", f"{filtered_df['valeur'].min():.2f}")
st.metric("Max", f"{filtered_df['valeur'].max():.2f}")

st.subheader("Carte des capteurs")
sensor_locations = get_sensors_with_location()

if not sensor_locations.empty:
    st.map(sensor_locations.rename(columns={"longitude": "lat", "latitude": "lon"}))
else:
    st.info("Aucune position de capteur disponible.")