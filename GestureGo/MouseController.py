import cv2
import mediapipe as mp
from pynput.mouse import Controller, Button

# Initialize MediaPipe hands and drawing modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Initialize mouse controller
mouse = Controller()

# Get the screen width and height
screen_width, screen_height = 1920, 1080  # Replace with your screen resolution

# Open webcam
cap = cv2.VideoCapture(0)

def map_value(value, left_min, left_max, right_min, right_max):
    # Map value from one range to another
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)
    return right_min + (value_scaled * right_span)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for natural interaction
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the landmarks of the index finger tip
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Convert the normalized coordinates to screen coordinates
            x = int(map_value(index_finger_tip.x, 0, 1, 0, screen_width))
            y = int(map_value(index_finger_tip.y, 0, 1, 0, screen_height))

            # Move the mouse cursor
            mouse.position = (x, y)

            # Detect pinch gesture for click
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Calculate the distance between the thumb tip and the index finger tip
            distance = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5

            # If the distance is small enough, perform a click
            if distance < 0.05:
                mouse.click(Button.left, 1)

    # Optionally, you can still draw hand landmarks for debugging
    # mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the OpenCV window
    # cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
