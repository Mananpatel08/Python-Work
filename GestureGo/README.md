# GestureGo: Gesture-Based Controllers

**GestureGo** is an innovative project designed to control media playback, presentation slides, and mouse movement using hand gestures. The project utilizes **MediaPipe** for hand gesture recognition and integrates it with **PyAutoGUI** and **Pynput** to control various applications on the computer. 

## Project Overview

The project is divided into three modules:

1. **Media Controller**: Use hand gestures to control media (play, pause, volume up/down).
2. **Presentation Controller**: Navigate PowerPoint slides with hand gestures.
3. **Mouse Controller**: Move the mouse pointer and click using hand gestures.

This project offers a touchless interaction experience, ideal for presentations, media control, and accessibility.

---

## Features

- **Media Controller**: 
  - Play/Pause media
  - Volume up/down
  - Skip media forward/backward
  
- **Presentation Controller**: 
  - Control slide navigation (next, previous)
  - Start/stop the presentation

- **Mouse Controller**: 
  - Move the cursor using hand gestures
  - Simulate left-click actions with a pinch gesture

---

## Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- PyAutoGUI (`pyautogui`)
- Pynput (`pynput`)
- Keyboard (`keyboard`) for controlling the camera feed

You can install the required libraries by running:

```bash
pip install opencv-python mediapipe pyautogui pynput keyboard
