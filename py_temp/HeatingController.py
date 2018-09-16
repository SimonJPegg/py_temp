import RPi.GPIO as GPIO
import logging as log
import datetime
import time


class HeatingController:

    def __init__(self, gpio_output_upstairs, gpio_output_downstairs, temp_monitor):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([gpio_output_upstairs, gpio_output_downstairs], GPIO.OUT)
        self.temp_monitor = temp_monitor
        self.__gpio_output_upstairs = gpio_output_upstairs
        self.__gpio_output_downstairs = gpio_output_downstairs

    # Turn the heating off
    def __set_heating_off(self, output_pin, location):
        GPIO.output(output_pin, 0)
        log.info('Heating set to off for: ' + location)

    # Turn the heating on
    def __set_heating_on(self, output_pin, location):
        GPIO.output(output_pin, 1)
        log.info('Heating set to on for: ' + location)

    # Set the heating on for 10 mins (if required) and turn it off again
    def __set_heating(self, output_pin, location):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(" Control for heating " + location + " set at: " + st)
        if all([self.temp_monitor.check_temperature(temp) for temp in self.temp_monitor.get_temperatures()]):
            self.__set_heating_on(output_pin, location)
        time.sleep(600)
        self.__set_heating_off(output_pin, location)

    # Set the heading for upstairs
    def set_heating_upstairs(self):
        self.__set_heating(self.__gpio_output_upstairs, 'Upstairs')

    # Set the heading for downstairs
    def set_heating_downstairs(self):
        self.__set_heating(self.__gpio_output_downstairs, 'Downstairs')