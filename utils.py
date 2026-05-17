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

def calculate_angle(a, b, c):
    angle = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    angle = abs(angle)
    if angle > 180.0:
        angle = 360.0 - angle
    return angle
