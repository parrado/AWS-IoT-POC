from time import sleep_ms
from mqtt import MQTTClient
from machine import Pin
import json
import dht
from machine import reset
from machine import deepsleep

# Pin object for user button
button = Pin (0, Pin.IN)

# If button is pressed finish script execution
if button.value()==1:
    
    try:

        # Pin object for user led 
        led=Pin(2,Pin.OUT)
        

        # Object for DHT22 management
        d = dht.DHT22(Pin(4))        

        # Read cetificate and private key from files for AWS IoT Core
        with open("certs/cert", 'rb') as f:
            certf = f.read()
        
        with open("certs/privkey", 'rb') as f:
            keyf = f.read()

        # Read AWS IoT Core endpoint address from file
        with open("certs/endpoint", 'r') as f:
            server = f.readline()            
        
        # MQTT client object
        client = MQTTClient(client_id="dht22_poc", server=server, port=8883, ssl=True, ssl_params={"cert":certf, "key":keyf})

        # Connect to IoT core
        client.connect()

        # Sensor measurement
        d.measure()
        temp=d.temperature()
        hum=d.humidity()
        print('Temperature %d ' %temp,' Humidity %d ' %hum)
        
        # Send data to IoT core
        print("Sending sensor data") 
        client.publish(topic="esp32/sensor", msg=json.dumps({"temp": int(temp),"hum": int(hum)}))
        
        # Disconnection procedure before going to deep sleep
        sleep_ms(1000)
        client.disconnect()
        sta_if.disconnect()
        sta_if.active(False)
               
        # Go to sleep     
        T=5000
        deepsleep(T)
        
    except:
        print('Error')
        reset()






