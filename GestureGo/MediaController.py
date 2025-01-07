import tkinter as tk
from tkinter import Label, Button
import cv2
import mediapipe as mp
import pyautogui
from PIL import Image, ImageTk
import threading

class GestureControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Gesture Video Controller")

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

        # Initialize video capture
        self.cap = cv2.VideoCapture(0)
        self.running = True

        # Create GUI elements
        self.video_label = Label(root)
        self.video_label.pack()

        self.stop_button = Button(root, text="Stop Video", command=self.stop_video)
        self.stop_button.pack(side="left", padx=10, pady=10)

        self.start_button = Button(root, text="Start Video", command=self.start_video)
        self.start_button.pack(side="right", padx=10, pady=10)

        # Start the video processing thread
        self.processing_thread = threading.Thread(target=self.process_video)
        self.processing_thread.start()

    def process_video(self):
        while self.running:
            if not self.cap.isOpened():
                break

            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                    # Extract landmarks
                    landmarks = [landmark for landmark in hand_landmarks.landmark]

                    # Define conditions for each gesture
                    thumb_up = landmarks[4].y < landmarks[3].y < landmarks[2].y
                    index_up = landmarks[8].y < landmarks[7].y < landmarks[6].y
                    middle_up = landmarks[12].y < landmarks[11].y < landmarks[10].y
                    ring_up = landmarks[16].y < landmarks[15].y < landmarks[14].y
                    pinky_up = landmarks[20].y < landmarks[19].y < landmarks[18].y

                    # Stop Video - Thumb Up Only
                    if thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
                        pyautogui.press('space')

                    # Volume Up - Four Fingers Up
                    # if not thumb_up and index_up and middle_up and ring_up and pinky_up:
                    if index_up and middle_up and ring_up and pinky_up:
                        pyautogui.press('up')

                    # Volume Down - Three Finger
                    if index_up and middle_up and ring_up and not pinky_up:
                        pyautogui.press('down')

                    # Skip 5 Seconds Back - Index Finger Up Only
                    if index_up and not middle_up and not ring_up and not pinky_up:
                        pyautogui.press('left')

                    # Skip 5 Seconds Forward - Index and Middle Fingers Up
                    if index_up and middle_up and not ring_up and not pinky_up:
                        pyautogui.press('right')

            # Convert the frame to an image format suitable for Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)

            self.video_label.config(image=photo)
            self.video_label.image = photo

            self.root.update_idletasks()
            self.root.update()

        self.cap.release()

    def start_video(self):
        if not self.processing_thread.is_alive():
            self.running = True
            self.processing_thread = threading.Thread(target=self.process_video)
            self.processing_thread.start()

    def stop_video(self):
        self.running = False
        self.cap.release()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GestureControllerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.stop_video)
    root.mainloop()
