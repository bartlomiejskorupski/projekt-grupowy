from random import choice, random
from time import sleep

DHT22 = 'DHT22'

def read_retry(sensor, pin) -> tuple[float, float]:
  retry_time = choice([0, 2, 4, 6])
  delta = (random()*2.0)-1.0
  humidity = random()*0.2 + 0.3
  # print('AAA MIMIMIMIMIMIMI')
  sleep(retry_time)
  # print('WOKE')
  return (humidity, 22 + delta)