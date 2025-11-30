import serial
import time

arduino = serial.Serial('COM3', 9600)
time.sleep(2) 

while True:
    data = arduino.readline().decode().strip()
    print("Sensor:", data)
