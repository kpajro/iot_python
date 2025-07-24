import streamlit as st
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="iot_database"
)

cursor = conn.cursor()

query = "SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 20"
cursor.execute(query)
results = cursor.fetchall()

columns = [i[0] for i in cursor.description]

df = pd.DataFrame(results, columns=columns)

st.title("Données météo")
st.dataframe(df)

cursor.close()
conn.close()
