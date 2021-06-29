import RPi.GPIO as GPIO
from time import sleep
import PySimpleGUI as sg
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv

img_layout = [[sg.Image("imgtest.png", key="_img_")]]

buttons_layout = [
                    [sg.Text(" ")],
                    [sg.Button("Forward", key="_forward_"), sg.Button("backwards", key="_backward_")],
                    [sg.Button("Turn left", key="_left_"), sg.Button("turn right", key="_right_")],
                    [sg.Button("Stop", key="_stop_"), sg.Exit(button_color=('white', 'firebrick'), key='Exit')]
                 ]

layout = [  [sg.Text("PiKart Controller", font=("Arial Light", 20, "bold"), justification="center", text_color="#125390", size=(48,1))],
            [sg.Column(img_layout, element_justification='c'), sg.Column(buttons_layout, element_justification='c')]
         ]

window = sg.Window("PiKart - Controller", layout, resizable=True, size=(500, 220))

# Pins for Motor Driver Inputs
class Controller:
    def __init__(self, MA1, MA2, MB1, MB2):
        MotorA1A = MA1
        MotorA2A = MA2
        MotorB1A = MB1
        MotorB2A = MB2
        self.setup()
    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)              # GPIO Numbering
        GPIO.setup(MotorA1A,GPIO.OUT)  # All pins as Outputs
        GPIO.setup(MotorA1B,GPIO.OUT)
        GPIO.setup(MotorB1A,GPIO.OUT)  # All pins as Outputs
        GPIO.setup(MotorB1B,GPIO.OUT)

    def forwardMA(self):
        GPIO.output(MotorA1A,GPIO.HIGH)
        GPIO.output(MotorA1B,GPIO.LOW)
        print("Going forwards with Motor A")
    def forwardMB(self):
        GPIO.output(MotorB1A,GPIO.HIGH)
        GPIO.output(MotorB1B,GPIO.LOW)
        print("Going forwards with Motor B")
    def backwardMB(self):
        GPIO.output(MotorB1A,GPIO.LOW)
        GPIO.output(MotorB1B,GPIO.HIGH)
        print("Going backwards with Motor B")
    def backwardMA(self):
        GPIO.output(MotorA1A,GPIO.LOW)
        GPIO.output(MotorA1B,GPIO.HIGH)
        print("Going bakcwards with Motor A")

    def stopall(self):
        GPIO.output(MotorA1A,GPIO.LOW)
        GPIO.output(MotorA1B,GPIO.LOW)
        GPIO.output(MotorB1B,GPIO.LOW)
        GPIO.output(MotorB1A,GPIO.LOW)
        print("Stopping all connected motors")

    def turn_right(self):
        self.forwardMA()
        self.backwardMB()
        print("Going right")
    def turn_left(self):
        self.forwardMB()
        self.backwardMA()
        print("Going left")

    def forward(self):
        self.forwardMB()
        self.forwardMA()
    def backward(self):
        self.backwardMB()
        self.backwardMA()

    def stopA(self):
        GPIO.output(MotorA1A,GPIO.LOW)
        GPIO.output(MotorA1B,GPIO.LOW)
        print("Stopped A motor")
    def stopB(self):
        GPIO.output(MotorB1A,GPIO.LOW)
        GPIO.output(MotorB1B,GPIO.LOW)
        print("Stopped A motor")
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)              # GPIO Numbering
    GPIO.setup(7,GPIO.OUT)  # All pins as Outputs
    GPIO.setup(8,GPIO.OUT)
def stopA():
    GPIO.output(7,GPIO.LOW)
    GPIO.output(8,GPIO.LOW)
    print("Stopped A motor")
def forwardMA():
    GPIO.output(7,GPIO.HIGH)
    GPIO.output(8,GPIO.LOW)
    print("Going forwards with Motor A2")
def backwardMA():
    GPIO.output(7,GPIO.HIGH)
    GPIO.output(8,GPIO.LOW)
    print("Going forwards with Motor A")

def destroy():
    MotorA1A = 38
    MotorA1B = 40
    MotorB1A = 35
    MotorB1B = 37
    Motor2A1A = 8
    Motor2A1B = 7
    control1 = Controller(MotorA1A, MotorA1B, MotorB1A, MotorB1B)
    control2 = Controller(MotorA1A, MotorA1B, 0, 0)
    control1.stopall()
    print("destroy called")
    control2.stopA()
    GPIO.cleanup()

try:
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
    camera.resolution = (224, 144)
    camera.start_preview()

    time.sleep(0.1)
    MotorA1A = 38
    MotorA1B = 40
    MotorB1A = 35
    MotorB1B = 37
    Motor2A1A = 7
    Motor2A1B = 8
    setup()
    control1 = Controller(MotorA1A, MotorA1B, MotorB1A, MotorB1B)
    control2 = Controller(MotorA1A, MotorA1B, 0, 0)
    while True:
        event, values = window.Read(timeout=1)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        rawCapture.truncate(0)
        imgbytes = cv.imencode('.png', image)[1].tobytes()
        window['_img_'].update(data=imgbytes)
        if event is None or event == 'Exit':
            control1.stopall()
            print("event none/exit")
            control2.stopA()
            GPIO.cleanup()
            break
        if event == "_forward_":
            control2.forwardMA()
            forwardMA()
            control1.forward()
        elif event == "_backward_":
            control1.backward()
            control2.backwardMA()

        elif event == "_stop_":
            control1.stopall()
            print("stop event sent")
            control2.stopA()
            stopA()
        elif event == "_left_":
            stopA()
            control1.turn_left()
        elif event == "_right_":
            stopA()
            control1.turn_right()
except Exception as e:
    destroy()
    print(e)
