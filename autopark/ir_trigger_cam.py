import RPi.GPIO as GPIO #import library to access GPIO pin
import time
from rpi_lcd import LCD
import math
from picamera import PiCamera
from time import sleep
from PIL import Image
import pytesseract
import cv2
import numpy as np
from pytesseract import Output
import os
import mysql.connector

mydb = mysql.connector.connect(
  host="capstone.cayk5wnefmpg.us-east-1.rds.amazonaws.com",
  user="admin",
  password="nuttertools"
)

IR_PIN= 11 #define pin for ir sensor
IR_PIN2= 13
IR_PIN3 = 15
IR_PINENTER = 18
IR_PINEXIT = 16

lcd=LCD()

GPIO.setmode(GPIO.BOARD) #consider complete rpi board
GPIO.setup(IR_PIN,GPIO.IN) #set pin function as input
GPIO.setup(IR_PIN2,GPIO.IN) #set pin function as input
GPIO.setup(IR_PIN3,GPIO.IN) #set pin function as input
GPIO.setup(IR_PINENTER,GPIO.IN) #set pin function as input
GPIO.setup(IR_PINEXIT,GPIO.IN) #set pin function as input



while True: #check if something is there
    if(GPIO.input(IR_PINENTER) == 0):  #IR SENSOR AT ENTRANCE NEAR LCD DISPLAY
        print("SLOT 1&2 RESERVED, SLOT3 AVAILABLE, IF RESERVED, PARK AT SLOT1&2 ELSE AT SLOT 3") #if car detected, 
        lcd.text("SLOT 1&2 RESERVED",1) #show spaces available
        lcd.text("SLOT 3 AVAILABLE",2)
        time.sleep(1)
    else:
        print("AUTOPARK") #if not show name
        lcd.text("AUTOPARK",1)
        time.sleep(2)
        
    if(GPIO.input(IR_PIN) == 0): #if slot 1 is taken 
        print("PARKING SLOT 1 IS OCCUPIED")
        message1 = "SLOT 1 TAKEN"
        lcd.text(message1,1)
        lcd.text("SLOT 2&3 FREE",2)
        time.sleep(0.25)
        lcd.text("2 SPOTS FREE",1)
        
        try:
            time.sleep(5)
            exec(open("slot1.py").read()) #go to slot1.py 
        except:
            print("error calling slot1.py")
        #exit() #camera exits
        time.sleep(1)
    else:
        print("PARKING SLOT 1 IS EMPTY")
        time.sleep(1)
    
    if(GPIO.input(IR_PIN2) == 0):
        print("PARKING SLOT 2 IS OCCUPIED")
        message2 = "SLOT 2 TAKEN"
        lcd.text(message2,1)
        lcd.text("SLOT 1&3 FREE",2)
        time.sleep(0.25)
        lcd.text("2 SPOTS FREE",1)
        try:
            time.sleep(5)
            exec(open("slot2.py").read())
        except:
            print("error calling slot2.py")
        #exit() #camera exits
        time.sleep(1)
        
    else:
        print("PARKING SLOT 2 IS EMPTY")
        time.sleep(1)
        
    if(GPIO.input(IR_PIN3) == 0):
        print("PARKING SLOT 3 IS OCCUPIED")
        message3 = "SLOT 3 TAKEN"
        print(message3)
        lcd.text(message3,1)
        lcd.text("SLOT 1 &2 FREE",2)
        time.sleep(0.25)
        lcd.text("2 SPOTS FREE",1)
        try:
            time.sleep(5)
            exec(open("slot2.py").read())
        except:
            print("error calling slot3.py")
        #exit() #camera exits
        time.sleep(1)
                
    else:
        print("PARKING SLOT 3 IS EMPTY")
        time.sleep(1)
    
    if(GPIO.input(IR_PINEXIT) == 0): 
        print("THANK YOU FOR PARKING")
        #lcd.text("SLOT 1&2 RESERVED",1)
        #lcd.text("SLOT 3 AVAILABLE",2)
        time.sleep(1)
        exec(open("exitlot.py").read())
        #lcd.text("THANK YOU FOR PARKING",1)
        #lcd.text("NO RESERVE: PARK AT 3",2)
    else:
        #print("AUTOPARK")
        #lcd.text("AUTOPARK",1)
        time.sleep(1 )
    

