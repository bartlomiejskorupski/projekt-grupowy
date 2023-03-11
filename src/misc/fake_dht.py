from random import choice, random
from time import sleep

DHT22 = 'DHT22'

last_reading = (53.59999847, 21,39999961)
max_reading = {
  'humidity': 70.0,
  'temperature': 30.0
}
min_reading = {
  'humidity': 40.0,
  'temperature': 15.0
}

temperature_change = 0.1
humidity_change = 0.1

def read_retry(sensor, pin) -> tuple[float, float]:
  global temperature_change, humidity_change, min_reading, max_reading, last_reading

  retry_time = choice([0, 2, 4, 6])

  hd = (random()*0.02)-0.01
  td = (random()*0.02)-0.01
  temperature_change = temperature_change + td
  humidity_change = humidity_change + hd

  last_reading = (
    min(max(last_reading[0] + humidity_change, min_reading['humidity']), max_reading['humidity']),
    min(max(last_reading[1] + temperature_change, min_reading['temperature']), max_reading['temperature'])
  )

  # print('AAA MIMIMIMIMIMIMI')
  sleep(retry_time)
  # print('WOKE')
  return last_reading