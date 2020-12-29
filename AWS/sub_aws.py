# importing libraries
import paho.mqtt.client as paho
import os
import socket
import ssl
import RPi.GPIO as GPIO
import time
import json
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)#xanh
def on_connect(client, userdata, flags, rc):                # func for making connection
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#" , 1 )                              # Subscribe to all topics
 
def on_message(client, userdata, msg):                      # Func for receiving msgs
    print("topic: "+msg.topic)
    x = json.loads(msg.payload)
    print("payload: "+x["message"])
    #while (True):
    if x["message"] == "ON" :
        GPIO.output(17, GPIO.HIGH)
    else :
        GPIO.output(17, GPIO.LOW)
    time.sleep(2)
    GPIO.output(17, GPIO.LOW)
    
#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log
#### Change following parameters #### 
awshost = "a2zr3tmxah1nq4-ats.iot.us-west-2.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "iotaws"                                     # Thing_Name
thingName = "iotaws"                                    # Thing_Name
caPath = "/home/pi/AWS/AmazonRootCA1.pem"                                      # Root_CA_Certificate_Name
certPath = "/home/pi/AWS/001697ea83-certificate.pem.crt"                            # <Thing_Name>.cert.pem
keyPath = "/home/pi/AWS/001697ea83-private.pem.key"                          # <Thing_Name>.private.key
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)      
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server

mqttc.loop_forever()

    
