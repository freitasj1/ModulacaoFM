import paho.mqtt.client as mqttClient
import time
import json
import tkinter as tk
from tkinter import ttk


frequencies = [87.70, 87.90, 88.10, 88.30, 88.50, 88.70, 88.90, 106.70, 106.90, 107.10, 107.30, 107.50, 107.70, 107.90]
areas = ["area-1", "area-2", "area-3", "area-4", "area-5"]
selected_frequency = None
selected_area = None
connected = False

BROKER_ENDPOINT = "industrial.api.ubidots.com"
PORT = 1883
MQTT_USERNAME = "BBUS-Cj0dkzpnTrzkHbWjFHUsDnu5liWOPO"
MQTT_PASSWORD = ""
TOPIC = "/v1.6/devices/"
DEVICE_LABEL = "places"


def submit_data():
    global selected_frequency, selected_area

    selected_frequency = frequency_var.get()
    selected_area = area_var.get()

    if selected_area and selected_frequency:
        print(f"Data Value: {selected_frequency}")
        print(f"Area: {selected_area}")
        main(mqtt_client) 

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[INFO] Connected to broker")
        global connected
        connected = True
    else:
        print("[INFO] Error, connection failed")

def on_publish(client, userdata, result):
    print("[INFO] Published!")

def connect(mqtt_client):
    
    mqtt_client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.connect(BROKER_ENDPOINT, port=PORT)
    mqtt_client.loop_start()

def publish(mqtt_client, topic, payload):
    try:
        mqtt_client.publish(topic, payload)
    except Exception as e:
        print(f"[ERROR] There was an error: {e}")

def main(mqtt_client):

    global selected_area, selected_frequency

    VARIABLE_LABEL = selected_area
    data_value = selected_frequency
    topic = TOPIC + DEVICE_LABEL
    payload = json.dumps({VARIABLE_LABEL: data_value})

    if not connected:
        connect(mqtt_client)

    print("[INFO] Attempting to publish payload:")
    print(payload)
    print("[INFO] Into Topic:")
    print(topic)
    publish(mqtt_client, topic, payload)


root = tk.Tk()
root.title("Escolha de Valores")

frame_frequency = tk.Frame(root)
frame_frequency.pack(pady=10)

tk.Label(frame_frequency, text="Escolha a frequência:").pack()

frequency_var = tk.DoubleVar(value=frequencies[0])
frequency_menu = ttk.Combobox(frame_frequency, textvariable=frequency_var, values=frequencies, state="readonly")
frequency_menu.pack()

frame_area = tk.Frame(root)
frame_area.pack(pady=10)

tk.Label(frame_area, text="Escolha a área:").pack()

area_var = tk.StringVar(value=areas[0])
area_menu = ttk.Combobox(frame_area, textvariable=area_var, values=areas, state="readonly")
area_menu.pack()

submit_button = tk.Button(root, text="Submit", command=submit_data)
submit_button.pack(pady=20)

mqtt_client = mqttClient.Client()  
connect(mqtt_client)   

root.mainloop()
