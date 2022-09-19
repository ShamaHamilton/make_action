'''Управление положением серводвигателя.'''


import RPi.GPIO as GPIO


servo_pin = 18

# Корректируем эти значения, чтобы серводвигатель вращался на полную мощность
deg_0_pulse = 0.544  # ms
deg_180_pulse = 2.4  # ms
f = 50.0  # 50Hz = 20ms between pulses

# Вычисляем широту ШИМ
period = 1000 / f  # 20ms
k = 100 / period  # duty 0..100 over 20ms
deg_0_duty = deg_0_pulse * k
pulse_range = deg_180_pulse - deg_0_pulse
duty_range = pulse_range * k

# Инициализируем контакт GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, f)
pwm.start(0)


def set_angle(angle):
    '''Преобразует величину угла в значение рабочего цикла, а затем
    вызывает ChangeDutyCycle для заданния новой длины импульса.'''
    duty = deg_0_duty + (angle / 180.0) * duty_range
    pwm.ChangeDutyCycle(duty)


try:
    while True:
        angle = int(input('Введите угол (0 - 180): '))
        set_angle(angle)
finally:
    print('Сброс')
    GPIO.cleanup()
