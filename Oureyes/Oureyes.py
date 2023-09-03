import openai
import time
import speech_recognition as sr
from gtts import gTTS
import os
import bluetooth
import cv2

class SmartGlasses:
    def __init__(self):
        self.openai_api_key = "YOUR_API_KEY_HERE"
        self.r = sr.Recognizer()
        self.device_address = None
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.camera_a = cv2.VideoCapture(0)
        self.camera_b = cv2.VideoCapture(1)

        self.detector = snowboydecoder.HotwordDetector("kristy.pmdl", sensitivity=0.5)

    def wake_word_callback(self):
        print("Kristy detected. How can I help you?")

    def generate_response(self, prompt):
        openai.api_key = self.openai_api_key
        model_engine = "davinci"
        prompt_text = prompt
        max_tokens = 60
        temperature = 0.7
        n = 1
        stop = None

        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt_text,
            max_tokens=max_tokens,
            temperature=temperature,
            n=n,
            stop=stop
        )

        ai_response = response.choices[0].text.strip()

        return ai_response

    def get_audio(self):
        with sr.Microphone() as source:
            audio = self.r.listen(source)
            try:
                input_text = self.r.recognize_google(audio)
                print("You said: " + input_text)
                return input_text
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def speak(self, text):
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        os.system("mpg123 response.mp3")

    def measure_distance(self):
        # TODO: Implement LiDAR distance measurement
        return 0

    def capture_image(self, camera):
        ret, img = camera.read()
        return img

    def connect_bluetooth(self):
        devices = bluetooth.discover_devices()
        for d in devices:
            if "My MacBook" in bluetooth.lookup_name(d):
                self.device_address = d
                break

        if self.device_address:
            self.sock.connect((self.device_address, 1))
            print("Bluetooth connection established.")
        else:
            print("Could not find device to connect to.")

    def run(self):
        self.detector.start(detected_callback=self.wake_word_callback, interrupt_check=None, sleep_time=0.03)
        self.connect_bluetooth()

        while True:
            input_text = self.get_audio()
            if not input_text:
                continue

            if "exit" in input_text.lower():
                break

            ai_response = self.generate_response(input_text)

            self.speak(ai_response)

            self.sock.send(ai_response.encode())

            distance = self.measure_distance()

            self.speak("The object is " + str(distance) + " steps away.")

            img_a = self.capture_image(self.camera_a)
            img_b = self.capture_image(self.camera_b)

            time.sleep(0.5)

        self.camera_a.release()
        self.camera_b.release()

        self.sock.close()
        print("Bluetooth connection closed.")

if __name__ == "__main__":
    smart_glasses = SmartGlasses()
    smart_glasses.run()
