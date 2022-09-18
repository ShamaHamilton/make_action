from tkinter import *
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

# Запускаем ШИМ
pwmRed = GPIO.PWM(18, 500)
pwmGreen = GPIO.PWM(23, 500)
pwmBlue = GPIO.PWM(24, 500)
pwmRed.start(100)
pwmGreen.start(100)
pwmBlue.start(100)


class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        # Создаем надписи и располагаем каждую в своей ячейке сетки.
        Label(frame, text='Red').grid(row=0, column=0)
        Label(frame, text='Green').grid(row=1, column=0)
        Label(frame, text='Blue').grid(row=2, column=0)

        # Создаем ползунки и располагаем каждый в своей ячейке сетки.
        scaleRed = Scale(
            frame, from_=0, to=100, orient=HORIZONTAL, command=self.updateRed)
        scaleRed.grid(row=0, column=1)

        scaleGreen = Scale(
            frame, from_=0, to=100, orient=HORIZONTAL, command=self.updateGreen)
        scaleGreen.grid(row=1, column=1)

        scaleBlue = Scale(
            frame, from_=0, to=100, orient=HORIZONTAL, command=self.updateBlue)
        scaleBlue.grid(row=2, column=1)

    def updateRed(self, duty):
        '''Change the led brightness to match the slider.'''
        pwmRed.ChangeDutyCycle(float(duty))

    def updateGreen(self, duty):
        '''Change the led brightness to match the slider.'''
        pwmGreen.ChangeDutyCycle(float(duty))

    def updateBlue(self, duty):
        '''Change the led brightness to match the slider.'''
        pwmBlue.ChangeDutyCycle(float(duty))


# Запускаем GUI, задаем для окна название, размер и положение.
root = Tk()
root.wm_title('RGB Led Control')
app = App(root)
root.geometry('200x150+0+0')
try:
    root.mainloop()
finally:
    print('Сброс')
    GPIO.cleanup()
