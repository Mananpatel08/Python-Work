import cv2
import mediapipe as mp
import pyautogui
import time
import keyboard  # Import the keyboard library

# Initialize MediaPipe hands and drawing modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Get the screen width and height
screen_width, screen_height = 1920, 1080  # Replace with your screen resolution

# Open webcam
cap = cv2.VideoCapture(0)

drawing = False  # Indicates whether drawing is active
previous_x, previous_y = None, None  # Previous coordinates for drawing

# Variable to control whether to display the camera feed
show_camera_feed = False


def map_value(value, left_min, left_max, right_min, right_max):
    # Map value from one range to another
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)
    return right_min + (value_scaled * right_span)


def is_finger_up(landmarks, hand_landmark):
    return landmarks[hand_landmark].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y


def control_powerpoint(gesture):
    if gesture == 'next_slide':
        pyautogui.press('right')
    elif gesture == 'previous_slide':
        pyautogui.press('left')
    elif gesture == 'start_slideshow':
        pyautogui.press('f5')
    elif gesture == 'stop_slideshow':
        pyautogui.press('esc')


def activate_pen_tool():
    pyautogui.hotkey('ctrl', 'p')


def deactivate_pen_tool():
    pyautogui.hotkey('ctrl', 'a')


# Ensure PowerPoint is in presentation mode and pen tool is activated
time.sleep(5)  # Give time to switch to PowerPoint
control_powerpoint('start_slideshow')
time.sleep(2)
activate_pen_tool()

while True:
    # Check for the stop key combination (Ctrl + Q)
    if keyboard.is_pressed('ctrl+q'):
        print("Stopping the script...")
        break

    # Check for the toggle key combination (Ctrl + T) to show/hide the camera feed
    if keyboard.is_pressed('ctrl+t'):
        show_camera_feed = not show_camera_feed
        time.sleep(0.5)  # Add a small delay to prevent rapid toggling

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

            # Check if the required fingers are up
            index_up = is_finger_up(hand_landmarks.landmark,
                                    mp_hands.HandLandmark.INDEX_FINGER_TIP)
            middle_up = is_finger_up(hand_landmarks.landmark,
                                     mp_hands.HandLandmark.MIDDLE_FINGER_TIP)
            ring_up = is_finger_up(hand_landmarks.landmark,
                                   mp_hands.HandLandmark.RING_FINGER_TIP)
            thumb_up = is_finger_up(hand_landmarks.landmark,
                                    mp_hands.HandLandmark.THUMB_TIP)
            pinky_up = is_finger_up(hand_landmarks.landmark,
                                    mp_hands.HandLandmark.PINKY_TIP)

            # Detect hand gestures for PowerPoint control
            if index_up and not middle_up and not ring_up and not thumb_up and not pinky_up:
                control_powerpoint('next_slide')
            elif index_up and middle_up and not ring_up and not thumb_up and not pinky_up:
                control_powerpoint('previous_slide')
            elif thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
                control_powerpoint('start_slideshow')
            elif not thumb_up and index_up and middle_up and ring_up and pinky_up:
                control_powerpoint('stop_slideshow')

            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect drawing gesture (pinch with middle finger up)
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            distance = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y -
                                                                   index_finger_tip.y) ** 2) ** 0.5
            if distance < 0.05 and middle_up and not ring_up and not pinky_up:
                drawing = True
            else:
                drawing = False
                previous_x, previous_y = None, None

            # Perform drawing if drawing mode is active
            if drawing:
                if previous_x is not None and previous_y is not None:
                    pyautogui.moveTo(x, y)
                    pyautogui.mouseDown()
                else:
                    pyautogui.moveTo(x, y)
                    pyautogui.mouseUp()
                    previous_x, previous_y = x, y

    # Display the resulting frame only if the toggle is enabled
    if show_camera_feed:
        cv2.imshow('Hand Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
