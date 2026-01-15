# boot module to connect to WiFi
import network
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    with open("certs/wifi", 'r') as f:
        creds = f.readline().split()       
        sta_if.connect(creds[0], creds[1])
        while not sta_if.isconnected():
            pass
print('network config:', sta_if.ifconfig())
    


