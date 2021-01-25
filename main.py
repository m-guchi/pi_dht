import RPi.GPIO as GPIO
import dht11
import time
import datetime
import requests
from requests.auth import HTTPBasicAuth

import sys
sys.path.append('../')
from config import basic,url

if __name__ == "__main__":

    pin_data = 4
    pin_led = 27

    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    instance = dht11.DHT11(pin=pin_data)

    GPIO.setup(pin_led, GPIO.OUT, initial=GPIO.LOW)

    error_num = 0
    max_error_num = 5

    while True:
        GPIO.output(pin_led, GPIO.HIGH)
        result = instance.read()
        if result.is_valid():
            url = url.SECRET + "/myroom/api/dht"
            auth = HTTPBasicAuth(basic.SECRET["user"], basic.SECRET["password"])
            params = {"time": str(datetime.datetime.now()), "temp" : result.temperature, "humid": result.humidity}
            req_session = requests.session()
            response =  req_session.post(url, data=params, auth=auth)
            with open('/home/guchi/dht/log.txt', 'a') as f:
                f.write(str(datetime.datetime.now()) + ": OK\n")
            time.sleep(0.5)
            GPIO.output(pin_led, GPIO.LOW)
            break
        else:
            time.sleep(0.3)
            GPIO.output(pin_led, GPIO.LOW)
            time.sleep(0.4)
            GPIO.output(pin_led, GPIO.HIGH)
            time.sleep(0.3)
            GPIO.output(pin_led, GPIO.LOW)
            error_num += 1
            if(error_num >= max_error_num):
                with open('/home/guchi/dht/log.txt', 'a') as f:
                    f.write(str(datetime.datetime.now()) + ": ERROR\n")
                break
            time.sleep(3)

    GPIO.cleanup()