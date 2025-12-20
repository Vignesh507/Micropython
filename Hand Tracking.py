import cv2
import mediapipe as mp
import serial
import time

# Change COM port
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        arduino.write(b'1')  # LED ON
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
        cv2.putText(frame, "HAND DETECTED - LED ON",
                    (10,40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,255,0), 2)
    else:
        arduino.write(b'0')  # LED OFF
        cv2.putText(frame, "NO HAND - LED OFF",
                    (10,40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,0,255), 2)

    cv2.imshow("Hand LED Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
