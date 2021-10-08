import threading
from DHT import *
import paho.mqtt.client as mqtt 
from random import uniform
import time
import json
import math
import random
import sys

channelPrefix = "trabalhopdd1110002203"
mqttBroker = "mqtt.eclipseprojects.io"

# Inicializa nó
def createNode():
    dht = DHT(mqttBroker, channelPrefix)
    print(f"#############addn {dht.nodeID}")

# cria dht inicial
def initDHT(nodeCount):
    for _ in range(nodeCount):
        t = threading.Thread(target=createNode)
        t.start()

def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload)
        if payload['type'] == 'server_response':
            print("CLIENT: Message recebida: " + str(message.payload))
    except:
        pass


def randomNodeGenerator():
    while True:
        num = int(random.uniform(1, 10))
        if (num == 1):
            t = threading.Thread(target=createNode)
            t.start()
        time.sleep(2)

#inicializa DHT
nodesCount = 8
if (len(sys.argv) > 1):
    print(sys.argv[1])
    nodesCount = int(float(sys.argv[1]))


initDHT(nodesCount)
threading.Thread(target=randomNodeGenerator).start()


#inicializa um cliente
client = mqtt.Client("trabalhopdd1110002203" + str(uniform(0, 10000000)))
client.connect(mqttBroker) 
client.loop_start()
client.on_message = on_message
client.subscribe(channelPrefix + '/hash')

def sendCommand(data):
    id = math.floor(uniform(0, 2**32 - 1))
    data['id'] = id
    data['key'] = int(data['key'])
    client.publish(channelPrefix + "/hash", json.dumps(data))
    print('Comando enviado. ID:' + str(data['id']))

def sendPut(key, text):
    data = {
        "type": 'put',
        "key": key,
        "value": text
    }
    sendCommand(data)

def sendGet(key):
    data = {
        "type": 'get',
        "key": key
    }
    sendCommand(data)

time.sleep(2)

print('CLIENT: Digite o que você deseja:')
print('CLIENT: put:[key]:[message]')
print('CLIENT: get:[key]')

while True:
    try:
        comands = input().split(':')
        if len(comands):
            if comands[0].lower() == 'put':
                if len(comands) >= 3:
                    sendPut(comands[1], ':'.join(comands[2:]))
                    continue
            elif comands[0].lower() == 'get':
                if len(comands) == 2:
                    sendGet(comands[1])
                    continue
        print('CLIENT: Comando inválido')
    except:
        print('CLIENT: Comando inválido')