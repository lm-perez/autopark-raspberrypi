import cv2
import pytesseract
import numpy as np
from pytesseract import Output
import mysql.connector
from rpi_lcd import LCD
from picamera import PiCamera

lcd=LCD()

mydb = mysql.connector.connect(
  host="capstone.cayk5wnefmpg.us-east-1.rds.amazonaws.com",
  user="admin",
  password="nuttertools"
)

camera = PiCamera() #camera is turned on
camera.start_preview()
time.sleep(3)
camera.stop_preview()
camera.resolution = (600, 360)
camera.exposure_mode = 'off'
path = "/home/pi/Desktop/autopark/pictures/"        
         
         # Camera warm-up time
sleep(0.1)
camera.capture(path+'exit.jpg')

def ifDetected(words):
    mycursor = mydb.cursor ()
    mycursor.execute("use capstone;")
    sql = "select LicensePlate from ReservedParking WHERE licensePlate = '{}' AND ParkingSlot = 1;".format(words)
    mycursor.execute(sql,)
    rows = mycursor.fetchone()
    if rows != None:
        data=mycursor.fetchall()
        print(rows[0])
    else :
        print("This is a reservation only slot, Kindly leave this slot as it is not reserved for you")
    mydb.close()
    
def onLeave(words):
    mycursor = mydb.cursor ()
    mycursor.execute("use capstone;")
    sql = "select * from ReservedParking WHERE licensePlate = '{}';".format(words)
    mycursor.execute(sql,)
    rows = mycursor.fetchone()
    print(words)
    if rows != None:
        ParkingSlot = rows[1]
        LicensePlate = rows[2]
        customerID = rows[3]
        EndDateTime = rows[4].strftime('%Y-%m-%d %H:%M:%S')
        StartDateTime = rows[5].strftime('%Y-%m-%d %H:%M:%S')
        sql = "DELETE FROM ReservedParking WHERE LicensePlate = '{}';".format(words)
        mycursor.execute(sql,)
        sql = "INSERT INTO ParkingHistory(LicensePlate,CustomerID,ParkingSlot,EntranceDate,ExitDate) VALUES('{}',{},{},'{}','{}');".format(LicensePlate,customerID,ParkingSlot,StartDateTime,EndDateTime)
        mycursor.execute(sql,)
        mydb.commit()
        print("%s is now leaving.",words)
        lcd.text("PARKING PAID BY:",1)
        lcd.text(words,2)
        time.sleep(0.25)
    else :
        print("Please Pay at the app")
        lcd.text("PLEASE PAY AT THE",1)
        lcd.text("AUTOPARK APP",2)
    mydb.close()
    
img=cv2.imread(path+'exit.jpg')
img=cv2.resize(img,(720,360))
crop=img[0:300,0:600]
gry=cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)
thr=cv2.threshold(gry,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
kernel = np.ones((5, 5), np.uint8)
opening=cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel)
words=pytesseract.image_to_string(opening)
platenum=words[0:8]
print(platenum)

onLeave(platenum)

cv2.imshow('img', opening)
#cv2.destroyAllWindows()
time.sleep(2)
#exec(open("ir_trigger_cam.py").read())
#cv2.waitKey(0)
