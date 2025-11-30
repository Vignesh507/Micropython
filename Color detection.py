import cv2
import serial
import time

# Arduino COM port (change COM3 to your port)
arduino = serial.Serial('COM8', 9600)
time.sleep(2)

cap = cv2.VideoCapture(0)

# Blue color range
lower_blue = (100, 150, 0)
upper_blue = (140, 255, 255)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Count number of blue pixels
    blue_count = cv2.countNonZero(mask)

    if blue_count > 5000:  
        arduino.write(b'1')   # LED ON
        print("LED ON")
    else:
        arduino.write(b'0')   # LED OFF
        print("LED OFF")
    
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
