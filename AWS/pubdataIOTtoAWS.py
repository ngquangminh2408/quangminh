#thu vien
from __future__ import print_function
from tkinter import *
#from tkinter.ttk import *
import tkinter.font as font
import time
from tkinter import messagebox
import Adafruit_DHT
import sys
import RPi.GPIO as GPIO
import paho.mqtt.client as paho
import os
# importing libraries
import socket
import ssl
import random
import string
import json
from random import uniform
connflag = False
#setmode va thong tin mqtt,global
GPIO.setmode(GPIO.BCM)
running = False  # Global flag
buttonMQClicked = False
buttonDHTClicked = False
buttonPIRClicked = False
buttonULTRAClicked = False
buttonLEDClicked = False
#mqttc.on_log = on_log
#### Change following parameters #### 
awshost = "a2zr3tmxah1nq4-ats.iot.us-west-2.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "iotaws"                                     # Thing_Name
thingName = "iotaws"                                    # Thing_Name
caPath = "/home/pi/AWS/AmazonRootCA1.pem"                                      # Root_CA_Certificate_Name
certPath = "/home/pi/AWS/001697ea83-certificate.pem.crt"                            # <Thing_Name>.cert.pem
keyPath = "/home/pi/AWS/001697ea83-private.pem.key"                          # <Thing_Name>.private.key
 
#time=str(time.asctime(time.gmtime()))
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))

#cac chuc nang cua he thong
mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
mqttc.loop_start()

def scanning():
    if running:
        from datetime import datetime
        now = datetime.now()
        ctime = now.strftime("%H:%M:%S")
        #print("Current Time =", current_time)# Only do this if the Stop button has not been clicked
        if buttonMQClicked:
            time.sleep(1)
            print ("mq is running")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(11,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(21,GPIO.OUT)
            GPIO.setup(20,GPIO.OUT)
            GPIO.setup(16,GPIO.OUT)
            i=0
            if GPIO.input(11)==1:
                ret="GAS GAS"
                GPIO.output(16,GPIO.LOW)
                GPIO.output(21,GPIO.HIGH)
                GPIO.output(16,GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(21,GPIO.LOW)
                GPIO.output(16,GPIO.LOW)
                paylodmsg0="{"
                paylodmsg1 = "\"Mes\": \""
                paylodmsg2 = "\", \"Time\": \""
                paylodmsg3="\"}"
                paylodmsg = "{} {} {} {} {} {}".format(paylodmsg0,paylodmsg1,ret,paylodmsg2,ctime,paylodmsg3)
                paylodmsg = json.dumps(paylodmsg) 
                paylodmsg_json = json.loads(paylodmsg)       
                mqttc.publish("iotaws", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
                print("msg send to AWS" ) # Print sent temperature msg on console
                print(paylodmsg_json)
                    
            else:
                ret="NO GAS"
                GPIO.output(20,GPIO.HIGH)
                GPIO.output(21,GPIO.LOW)
                GPIO.output(16,GPIO.LOW)
                time.sleep(0.5)
                GPIO.output(20,GPIO.LOW)  
                paylodmsg0="{"
                paylodmsg1 = "\"Mes\": \""
                paylodmsg2 = "\", \"Time\": \""
                paylodmsg3="\"}"
                paylodmsg = "{} {} {} {} {} {}".format(paylodmsg0,paylodmsg1,ret,paylodmsg2,ctime,paylodmsg3)
                paylodmsg = json.dumps(paylodmsg) 
                paylodmsg_json = json.loads(paylodmsg)       
                mqttc.publish("iotaws", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
                print("msg send to AWS" ) # Print sent temperature msg on console
                print(paylodmsg_json)
            #return rs
        elif buttonDHTClicked:
            time.sleep(2)
            print ("dht is running")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(21, GPIO.OUT)         #LED output pin
            GPIO.setup(20, GPIO.OUT)
            GPIO.setup(16, GPIO.OUT)
            GPIO.setwarnings(False)
            DHT_SENSOR = Adafruit_DHT.DHT11
            DHT_PIN = 26
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                ret=str("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
                paylodmsg0="{"
                paylodmsg1 = "\"Mes\": \""
                paylodmsg2 = "\", \"Time\": \""
                paylodmsg3="\"}"
                paylodmsg = "{} {} {} {} {} {}".format(paylodmsg0,paylodmsg1,ret,paylodmsg2,ctime,paylodmsg3)
                paylodmsg = json.dumps(paylodmsg) 
                paylodmsg_json = json.loads(paylodmsg)       
                mqttc.publish("iotaws", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
                print("msg send to AWS" ) # Print sent temperature msg on console
                print(paylodmsg_json)
                #ret=client.publish("house",time)
                if  temperature<30:
                    GPIO.output(21,GPIO.LOW)
                    GPIO.output(20,GPIO.HIGH)
                    time.sleep(1.5)
                else:
                    GPIO.output(21,GPIO.HIGH)
                    GPIO.output(20,GPIO.LOW)
                    time.sleep(1.5)
                #return rs
                    
                
            else:
                ret=str("Failed to retrieve data from humidity sensor")
                GPIO.output(20,GPIO.HIGH)
                GPIO.output(21,GPIO.HIGH)
                time.sleep(1.5)
                #return rs
                paylodmsg0="{"
                paylodmsg1 = "\"Mes\": \""
                paylodmsg2 = "\", \"Time\": \""
                paylodmsg3="\"}"
                paylodmsg = "{} {} {} {} {} {}".format(paylodmsg0,paylodmsg1,ret,paylodmsg2,ctime,paylodmsg3)
                paylodmsg = json.dumps(paylodmsg) 
                paylodmsg_json = json.loads(paylodmsg)       
                mqttc.publish("iotaws", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
                print("msg send to AWS" ) # Print sent temperature msg on console
                print(paylodmsg_json)
            GPIO.cleanup()
        elif buttonPIRClicked:
            time.sleep(1)
            print ("pir is running")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(10, GPIO.IN)       #Read output from PIR motion sensor
            GPIO.setup(21, GPIO.OUT)         #LED output pin
            GPIO.setup(20, GPIO.OUT)
            GPIO.setup(16, GPIO.OUT)
            i=GPIO.input(10)
            if i==0:                 #When output from motion sensor is LOW
                GPIO.output(21,GPIO.LOW)
                time.sleep(0.5)
                ret="KHONG CO CHUYEN DONG"
                #return "No intruders"
                paylodmsg0="{"
                paylodmsg1 = "\"Mes\": \""
                paylodmsg2 = "\", \"Time\": \""
                paylodmsg3="\"}"
                paylodmsg = "{} {} {} {} {} {}".format(paylodmsg0,paylodmsg1,ret,paylodmsg2,ctime,paylodmsg3)
                paylodmsg = json.dumps(paylodmsg) 
                paylodmsg_json = json.loads(paylodmsg)       
                mqttc.publish("iotaws", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
                print("msg send to AWS" ) # Print sent temperature msg on console
                print(paylodmsg_json)
            elif i==1:               #When output from motion sensor is HIGH
                GPIO.output(21,GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(21,GPIO.LOW)
                #return "Intruder detected"
                ret="CO CHUYEN DONG"
                paylodmsg0="{"
                paylodmsg1 = "\"Mes\": \""
                paylodmsg2 = "\", \"Time\": \""
                paylodmsg3="\"}"
                paylodmsg = "{} {} {} {} {} {}".format(paylodmsg0,paylodmsg1,ret,paylodmsg2,ctime,paylodmsg3)
                paylodmsg = json.dumps(paylodmsg) 
                paylodmsg_json = json.loads(paylodmsg)       
                mqttc.publish("iotaws", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
                print("msg send to AWS" ) # Print sent temperature msg on console
                print(paylodmsg_json)
            i=0
            GPIO.cleanup()

        elif buttonULTRAClicked:
            #time.sleep(1)
            print ("ultra is running")
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO_TRIGGER = 5
            GPIO_ECHO    = 6
            GPIO.setup(GPIO_TRIGGER,GPIO.OUT )  # Trigger
            GPIO.setup(GPIO_ECHO,GPIO.IN) 
            #GPIO.setmode(GPIO.BCM)
            GPIO.setup(21, GPIO.OUT)         #LED output pin
            GPIO.setup(20, GPIO.OUT)
            #temperature = 25
            #speedSound = 33100 + (0.6*temperature)
            GPIO.output(GPIO_TRIGGER, True)
            time.sleep(0.5)
            GPIO.output(GPIO_TRIGGER, False)
            time.sleep(0.00001)
            start = time.time()
            while GPIO.input(GPIO_ECHO)==0:
                start = time.time()
            while GPIO.input(GPIO_ECHO)==1:
                stop = time.time()
            elapsed = stop-start
            #print('time distance  :',elapsed)
            distance = elapsed * 33400
            distance = distance/2
            #print(distance)
            ret= str("Distance : {0:5.1f}".format(distance))
            paylodmsg0="{"
            paylodmsg1 = "\"Mes\": \""
            paylodmsg2 = "\", \"Time\": \""
            paylodmsg3="\"}"
            paylodmsg = "{} {} {} {} {} {}".format(paylodmsg0,paylodmsg1,ret,paylodmsg2,ctime,paylodmsg3)
            paylodmsg = json.dumps(paylodmsg) 
            paylodmsg_json = json.loads(paylodmsg)       
            mqttc.publish("iotaws", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
            print("msg send to AWS" ) # Print sent temperature msg on console
            print(paylodmsg_json)
            if distance > 10:
                GPIO.output(21,GPIO.LOW)
                GPIO.output(20,GPIO.HIGH)
                time.sleep(1)
                GPIO.output(20,GPIO.LOW)
            else :
                GPIO.output(20,GPIO.LOW)
                GPIO.output(21,GPIO.HIGH)
                time.sleep(1)
                GPIO.output(21,GPIO.LOW)
            GPIO.cleanup()
            
        elif buttonLEDClicked:
            time.sleep(1)
            print ("led is running")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17,GPIO.OUT)#xanh
            GPIO.setup(27,GPIO.OUT)#do
            GPIO.setup(22,GPIO.OUT)#vang
            GPIO.setwarnings(False)
            GPIO.output(17, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(17, GPIO.LOW)
            ret="GREEN HIGH"
            paylodmsg0="{"
            paylodmsg1 = "\"Mes\": \""
            paylodmsg2 = "\", \"Time\": \""
            paylodmsg3="\"}"
            paylodmsg = "{} {} {} {} {} {}".format(paylodmsg0,paylodmsg1,ret,paylodmsg2,ctime,paylodmsg3)
            paylodmsg = json.dumps(paylodmsg) 
            paylodmsg_json = json.loads(paylodmsg)       
            mqttc.publish("iotaws", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
            print("msg send to AWS" ) # Print sent temperature msg on console
            print(paylodmsg_json)
            time.sleep(1)
            GPIO.output(27, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(27, GPIO.LOW)
            ret="RED HIGH"
            paylodmsg0="{"
            paylodmsg1 = "\"Mes\": \""
            paylodmsg2 = "\", \"Time\": \""
            paylodmsg3="\"}"
            paylodmsg = "{} {} {} {} {} {}".format(paylodmsg0,paylodmsg1,ret,paylodmsg2,ctime,paylodmsg3)
            paylodmsg = json.dumps(paylodmsg) 
            paylodmsg_json = json.loads(paylodmsg)       
            mqttc.publish("iotaws", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
            print("msg send to AWS" ) # Print sent temperature msg on console
            print(paylodmsg_json)
            time.sleep(1)
            GPIO.output(22, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(22, GPIO.LOW)
            ret="YELLOW HIGH"
            paylodmsg0="{"
            paylodmsg1 = "\"Mes\": \""
            paylodmsg2 = "\", \"Time\": \""
            paylodmsg3="\"}"
            paylodmsg = "{} {} {} {} {} {}".format(paylodmsg0,paylodmsg1,ret,paylodmsg2,ctime,paylodmsg3)
            paylodmsg = json.dumps(paylodmsg) 
            paylodmsg_json = json.loads(paylodmsg)       
            mqttc.publish("iotaws", paylodmsg_json , qos=1)        # topic: temperature # Publishing Temperature values
            print("msg send to AWS" ) # Print sent temperature msg on console
            print(paylodmsg_json)
            time.sleep(1)
            GPIO.cleanup()
    # After 1 second, call scanning again (create a recursive loop)
    root.after(1000, scanning)  

#su kien cua button MQ135 
def start():
    """Enable scanning by setting the global flag to True."""
    global running
    global buttonMQClicked
    global buttonDHTClicked
    global buttonPIRClicked
    global buttonULTRAClicked
    global buttonLEDClicked
    running = True
    buttonDHTClicked = False
    buttonPIRClicked = False
    buttonULTRAClicked = False
    buttonLEDClicked = False
    buttonMQClicked = True
    root.after(1000, scanning)

#su kien cua button DHT
def startDHT():
    """Enable scanning by setting the global flag to True."""
    global running
    global buttonMQClicked
    global buttonDHTClicked
    global buttonPIRClicked
    global buttonULTRAClicked
    global buttonLEDClicked
    running = True
    buttonMQClicked = False
    buttonPIRClicked = False
    buttonULTRAClicked = False
    buttonLEDClicked = False
    buttonDHTClicked = True
    root.after(2000, scanning)

#su kien cua button PIR
def startPIR():
    """Enable scanning by setting the global flag to True."""   
    global running
    global buttonMQClicked
    global buttonDHTClicked
    global buttonPIRClicked
    global buttonULTRAClicked
    global buttonLEDClicked
    running = True
    buttonMQClicked = False
    buttonULTRAClicked = False
    buttonLEDClicked = False
    buttonDHTClicked = False
    buttonPIRClicked = True
    root.after(1000, scanning)

#su kien cua button Ultrasonic
def startULTRA():
    """Enable scanning by setting the global flag to True."""
    global running
    global buttonMQClicked
    global buttonDHTClicked
    global buttonPIRClicked
    global buttonULTRAClicked
    global buttonLEDClicked
    running = True
    buttonMQClicked = False
    buttonLEDClicked = False
    buttonDHTClicked = False
    buttonPIRClicked = False
    buttonULTRAClicked = True
    root.after(1000, scanning)

#su kien cua button Led
def startLED():
    """Enable scanning by setting the global flag to True."""
    global running
    global buttonMQClicked
    global buttonDHTClicked
    global buttonPIRClicked
    global buttonULTRAClicked
    global buttonLEDClicked
    running = True
    buttonMQClicked = False
    buttonDHTClicked = False
    buttonPIRClicked = False
    buttonULTRAClicked = False
    buttonLEDClicked = True
    root.after(1000, scanning)

#su kien cua button STOP
def stop():
    """Stop scanning by setting the global flag to False."""
    global running
    global buttonMQClicked
    global buttonDHTClicked
    global buttonPIRClicked
    global buttonULTRAClicked
    global buttonLEDClicked
    running = False
    buttonMQClicked = False
    buttonDHTClicked = False
    buttonPIRClicked = False
    buttonULTRAClicked = False
    buttonLEDClicked = False
    print("STOP")
    time.sleep(2)
    #root.destroy()

#GUI 
root = Tk()
root.title("NHOM 1")
root.geometry("880x400")

app = Frame(root)
app.grid()
myFont = font.Font(size=14)
myFontLabel = font.Font(size=18)

LB =Label(app,text="Nhom 1\nNguyen Quang Minh\nNguyen Le Minh Hieu\nHem Linh Chi\nHuynh Tuan Kiet",font = myFontLabel)
start = Button(app, text="MQ Scan", command=start,width=20,height=3,bg="grey",fg="white")
dht = Button(app, text="DHT Scan", command=startDHT,width=20,height=3,bg="grey",fg="white")
pir = Button(app, text="PIR Scan", command=startPIR,width=20,height=3,bg="grey",fg="white")
ultra = Button(app, text="ULTRASONIC Scan", command=startULTRA,width=20,height=3,bg="grey",fg="white")
led = Button(app, text="LED start", command=startLED,width=20,height=3,bg="grey",fg="white")
stop = Button(app, text="STOP", command=stop,width=20,height=3,bg="lightgrey",fg="white")

start['font'] = myFont
dht['font'] = myFont
pir['font'] = myFont
led['font'] = myFont
ultra['font'] = myFont
stop['font'] = myFont

LB.grid(row =0,column=2,pady=10,padx=10)
start.grid(row =1,column=3,pady=10,padx=10)
dht.grid(row =1,column=2,pady=10,padx=10)
pir.grid(row =2,column=1,pady=10,padx=10)
ultra.grid(row =2,column=2,pady=10,padx=10)
led.grid(row =1,column=1,pady=10,padx=10)
stop.grid(row =2,column=3,pady=10,padx=10)

#root.after(1000, scanningMQ)  # After 1 second, call scanning
root.mainloop()