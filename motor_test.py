import serial
import time

#calibrate the camera position
ser = serial.Serial('COM3', 9600)
while(1):
    inputSer = input("Enter a character: ")[0]
    ser.write(inputSer.encode())
    if(inputSer == 'w'):
        break

#begin doing algorithm stuff

print("Start\n")
#direction, speed, time
#speed * 25 (max is 255, but only up to 9*25)
#time * 250 (quarter of second)
ser.write(("a31").encode())

ser.close()
