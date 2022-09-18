'''Управление скоростью двигателя постоянного тока.'''


import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

control_pin = 18
GPIO.setup(control_pin, GPIO.OUT)
motor_pwm = GPIO.PWM(control_pin, 500)
motor_pwm.start(0)

try:
    while True:
        duty = int(input('Enter Duty Cycle (0 to 100): '))
        if duty < 0 or duty > 100:
            print('0 to 100')
        else:
            motor_pwm.ChangeDutyCycle(duty)
finally:
    print('Сброс')
    GPIO.cleanup()
