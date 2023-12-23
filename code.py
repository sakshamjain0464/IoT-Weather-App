import network
import socket
from time import sleep
import urequests as r
import dht
from machine import Pin
import ujson


ssid = 'Airel_9893111604'
password = 'air66793'

led = Pin(15, Pin.OUT)
led.value(0)
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        print(wlan.status())
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


try:
    ip = connect()
except KeyboardInterrupt:
    machine.reset()

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)


led.value(1)

sensor = dht.DHT11(Pin(16))

def getData():
    sensor.measure()  # Read sensor data
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pico W Weather Station</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: url('https://img.freepik.com/free-vector/flat-design-monsoon-season-clouds-illustration_23-2149424294.jpg?size=626&ext=jpg') center;
            background-size: cover;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .card {
            width: 50&percnt;;
            background-color: #ffffff00;
            border-radius: 8px;
            box-shadow: 20px 100px 100px 100px rgba(73, 70, 70, 0.1);
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(5px) saturate(177&percnt;);
            -webkit-backdrop-filter: blur(25px) saturate(177&percnt;);
        }

        h1 {
            color: #1B4F72;
        }

        p {
            color: #001929;
        }

        .data {
            font-size: 24px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>My Weather Station</h1>
        <p>Current Temperature and Humidity</p>
        <div class="data">
            <p id="temperature">%s&degC</p>
            <p id="humidity">%s &percnt;</p>
        </div>
    </div>

</body>
</html>
'''%(temperature, humidity)
    return html


def sendData(client):
    response = getData()
    client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    client.send(response)

    led.value(0)
    sleep(0.5)
    led.value(1)
while True:
    try:
        client, addr = s.accept()
        print('client connected from', addr)
        sendData(client)
        client.close()
        
    except OSError as e:
        client.close()
        print('connection closed')
    
    
