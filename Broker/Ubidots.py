import paho.mqtt.client as mqtt
import json
import time
import serial

# Configurações do broker MQTT
BROKER = 'industrial.api.ubidots.com'
PORT = 1883
DEVICE_LABEL = "places"
VARIABLE_PUBLISH = "frequencia-atual"
USERNAME = 'BBUS-Cj0dkzpnTrzkHbWjFHUsDnu5liWOPO'
PASSWORD = None  # Não há senha

# Inicializa a conexão serial
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)

# Função para ler e montar o valor da serial
def available():
    print(ser.name)
    b = 0
    x = ""
    while b != 'x':
        b = ser.read().decode('utf-8', errors='ignore')
        if b == ';':
            break
        else:
            x += b
            print(x)
    return x

# Função callback quando a mensagem é recebida
def on_message(client, userdata, msg):
    global data_value
    message = msg.payload.decode()
    print(f"Mensagem recebida: {message}")
    try:
        data = json.loads(message)
        data_value = data["value"]
        print(f"Recebido e processado valor: {data_value}")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON: {message}")

# Função callback quando a inscrição é realizada
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Inscrição realizada com sucesso: ID da inscrição: {mid}, QoS concedido: {granted_qos}")

# Função para publicar uma mensagem
def publish(mqtt_client, topic, payload):
    try:
        mqtt_client.publish(topic, payload)
        print('Sucesso ao publicar')
    except Exception as e:
        print(f"[ERROR] There was an error, details: \n{e}")

# Função principal
def main():
    
    while True:
        
        global data_value
        
        # Lê o valor da serial
        infoArea = ''
        while infoArea not in ['area-1', 'area-2', 'area-3', 'area-4', 'area-5']:
            print('Esperando a inserção da área...')
            infoArea = available()
        print(f'Área recebida: {infoArea}')

        # Configura tópicos com base no valor lido da serial
        TOPIC_SUBSCRIBE = f"/v1.6/devices/{DEVICE_LABEL}/{infoArea}"
        TOPIC_PUBLISH = f"/v1.6/devices/{DEVICE_LABEL}/{VARIABLE_PUBLISH}"

        
        client = mqtt.Client()
        client.on_message = on_message
        client.on_subscribe = on_subscribe
        client.username_pw_set(USERNAME, PASSWORD)
        client.connect(BROKER, PORT)
        client.loop_start()

        
        client.subscribe(TOPIC_SUBSCRIBE)
        
        
        print("Aguardando mensagem...")
        time.sleep(1)

        if data_value is not None:
            
            payload = json.dumps({"value": data_value})
            print(f'Publicando no tópico: {TOPIC_PUBLISH}. Payload: {payload}')
            publish(client, TOPIC_PUBLISH, payload)
            data_str = str(data_value)
            
            ser.write(data_str.encode('utf-8'))
            ser.write(b'\n')
            time.sleep(0.5) 
            response = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Mensagem enviada: {payload}")
            print(f"Resposta recebida: {response}")
        else:
            print("Nenhum valor recebido para publicação.")

        
        time.sleep(2)

        
        
        
        repeat = input("Deseja repetir o processo? (s/n): ").strip().lower()
        if repeat == 'n':
            print("Encerrando...")
            client.loop_stop()  
            client.disconnect()  
            ser.close()  
            break
        elif repeat == 's':
            print("Reiniciando o processo...")
            data_value = None  
            continue  
        else:
            print("Resposta inválida. Digite 's' para sim ou 'n' para não.")

if __name__ == "__main__":
    main()
