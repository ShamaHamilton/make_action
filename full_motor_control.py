'''Управление направлением и скоростью вращения двигателя. Микросхема L293D.'''


import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

enable_pin = 18
in_1_pin = 23
in_2_pin = 24

GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(in_1_pin, GPIO.OUT)
GPIO.setup(in_2_pin, GPIO.OUT)
motor_pwm = GPIO.PWM(enable_pin, 500)
motor_pwm.start(0)


def forward(duty):
    GPIO.output(in_1_pin, True)
    GPIO.output(in_2_pin, False)
    motor_pwm.ChangeDutyCycle(duty)


def reverse(duty):
    GPIO.output(in_1_pin, False)
    GPIO.output(in_2_pin, True)
    motor_pwm.ChangeDutyCycle(duty)


def stop():
    GPIO.output(in_1_pin, False)
    GPIO.output(in_2_pin, False)
    motor_pwm.ChangeDutyCycle(0)


try:
    while True:
        direction = input(
            'Enter direction letter (f - forward, r - reverse, s - stop): ')
        if direction[0] == 's':
            stop()
        else:
            duty = int(input('Enter Duty (0 to 100): '))
            if direction[0] == 'f':
                forward(duty)
            elif direction[0] == 'r':
                reverse(duty)
finally:
    print('Сброс')
    GPIO.cleanup()
