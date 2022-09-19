''' Термостатический ПИД-регулятор. Датчик температуры - DS18B20.'''


import os
import glob
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

heat_pin = 18
# определяем каталог, в котором находится файл для DS18В20.
base_dir = 'sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

GPIO.setup(heat_pin, GPIO.OUT)
heat_pwm = GPIO.PWM(heat_pin, 500)
heat_pwm.start(0)

# Глобальные переменные для ПИД-алгоритма
# old_error служит для вычисления изменения рассогласования для D-составляющей
old_error = 0
old_time = 0
measured_temp = 0
p_term = 0
i_term = 0
d_term = 0


def read_temp_raw():
    '''Считывает в виде двух строк текста показания микросхемы DS18B20.'''
    with open(device_file, 'r') as f:
        lines = f.readlines()
    # f = open(device_file, 'r')
    # lines = f.readlines()
    # f.close()
    return lines


def read_temp():
    '''Отвечает за фактическое извлечение показателя температуры с конца
    второй строки - после проверки, что в первой строке получен ответ YES.'''
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def constrain(value: int, min: int, max: int) -> int:
    '''Ограничивает значение первого параметра, чтобы оно всегда находилось
    внутри диапазона, указанного вторым и третьим параметрами.'''
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value


def update_pid():
    '''ПИД - вычисления.'''
    global old_time, old_error, measured_temp, set_temp, p_term, i_term, d_term
    now = time.time()
    # dt - сколько времени прошло с последнего вызова функции update_pid
    dt = now - old_time
    error = set_temp - measured_temp  # вычисление рассогласования
    de = error - old_error  # вычисление изменения в рассогласовании

    # вычисление составляющих
    p_term = kp * error
    i_term += ki * error
    i_term = constrain(i_term, 0, 100)
    d_term = (de / dt) * kd

    old_error = error
    # print(measured_temp, p_term, i_term, d_term)
    output = p_term + i_term + d_term
    output = constrain(output, 0, 100)
    return output


set_temp = int(input('Введите заданную температуру в градусах Цельсия '))
kp = int(input('kp: '))
ki = int(input('ki: '))
kd = int(input('kd: '))

old_time = time.time()


try:
    while True:
        # Если со времени предыдущего замера прошла 1 секунда,
        # производится измерение температуры, а затем получение нового
        # значения на выходе (duty) и соответствующее изменение
        # коэффициента заполнения ШИМ-канала.
        now = time.time()
        if now > old_time + 1:
            old_time = now
            measured_temp = read_temp()
            duty = update_pid()
            heat_pwm.ChangeDutyCycle(duty)
            print(f'{measured_temp}, {set_temp}, {duty}')
finally:
    GPIO.cleanup()
