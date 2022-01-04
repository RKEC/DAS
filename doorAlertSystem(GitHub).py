import smtplib
import time
from datetime import datetime
import board
import busio
import adafruit_vl6180x

time.sleep(2)
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl6180x.VL6180X(i2c)

door = False
count = 0

def sendMsg(msg):
    conn = smtplib.SMTP('smtp.gmail.com',587)
    conn.ehlo()
    conn.starttls()
    conn.login('from email', 'password')
    conn.sendmail('to email','to email',f'Subject: Alert! \n\n Door {msg} at {(datetime.now()).strftime("%H:%M:%S")}')
    conn.quit()


while True:
    range_mm = sensor.range
    print("Range: {0}mm".format(range_mm))
    if range_mm == 0  and door == False:
        count += 1
        print("Activated")
        if count % 2 == 0:
            msg = "Closed"
        else:
            msg = "Opened"
        sendMsg(msg)
        door = True
    
    elif range_mm == 255:
        door = False

    time.sleep(.25)

