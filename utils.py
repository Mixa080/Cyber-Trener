import threading
import pyttsx3
import math

def speak_async(text):
    def run_speech():
        try:
            import pythoncom
            pythoncom.CoInitialize()
            engine = pyttsx3.init()

            voices = engine.getProperty('voices')
            for voice in voices:
                if 'pl' in voice.languages or 'polish' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break

            engine.setProperty('rate', 150)
            engine.say(text)
            engine.runAndWait()
        except RuntimeError:
            pass
        except Exception:
            pass

    threading.Thread(target=run_speech, daemon=True).start()

def play_success_sound_async():
    def run_sound():
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_OK)
        except Exception:
            pass
    threading.Thread(target=run_sound, daemon=True).start()

def calculate_angle(a, b, c):
    angle = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    angle = abs(angle)
    if angle > 180.0:
        angle = 360.0 - angle
    return angle

import cv2
import numpy as np

def draw_centered_transparent_text(img, text, font_scale=1.0, thickness=2, color=(255, 255, 255), bg_color=(0, 0, 0), alpha=0.5, y_offset=0):
    if not text:
        return img
        
    overlay = img.copy()
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size, baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    text_w, text_h = text_size
    img_h, img_w = img.shape[:2]
    
    x = (img_w - text_w) // 2
    y = (img_h + text_h) // 2 + y_offset
    
    # Draw background rectangle
    padding = 10
    cv2.rectangle(overlay, 
                  (x - padding, y - text_h - padding), 
                  (x + text_w + padding, y + baseline + padding), 
                  bg_color, 
                  -1)
                  
    # Blend the overlay with the original image
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    
    # Draw the text on top (fully opaque)
    cv2.putText(img, text, (x, y), font, font_scale, color, thickness)
    
    return img

class CameraThread:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.ret = False
        self.frame = None
        self.running = True
        # Read the first frame
        self.ret, self.frame = self.cap.read()
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.ret = ret
                self.frame = frame

    def read(self):
        # Return a copy to avoid race conditions with drawing
        if self.frame is not None:
            return self.ret, self.frame.copy()
        return self.ret, self.frame

    def release(self):
        self.running = False
        self.thread.join(timeout=1)
        self.cap.release()
