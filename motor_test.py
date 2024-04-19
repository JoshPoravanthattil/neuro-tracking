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

#direction(a or d), power (0-255, increment by 25), time (1/4 s per unit)
ser.write(("a31").encode())

ser.write(("gxx").encode())
ser.write(("rxx").encode())

ser.close()
