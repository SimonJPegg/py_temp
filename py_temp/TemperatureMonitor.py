import os
import logging as log
import glob


class TemperatureMonitor:

    def __init__(self, error_temp, min_temp, max_temp, set_heating_below_max):
        self.__check_admin()
        self.__do_modprobe()
        self.__error_temp = error_temp
        self.__min_temp = min_temp
        self.__max_temp = max_temp
        self.__set_heating_below_max = set_heating_below_max

    # Check for admin
    def __check_admin(self):
        if os.getuid() != 0:
            log.error('this script requires admin rights.')
            log.error('please return script with command:')
            log.error('sudo ' + os.path.realpath(__file__))
            exit(-1)

    # Load the required linux system modules
    def __do_modprobe(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

    # get a list of files containing the temperatures
    def __get_input_files(self):
        base_dir = '/sys/bus/w1/devices/'
        files = [f + '/w1_slave' for f in glob.glob(base_dir + '28*')]
        return files

    # Read the contents of the passed in file
    def __read_file_contents(self, f):
        f = open(f, 'r')
        lines = f.readlines()
        f.close()
        return lines

    # Extract the temperature from the passed in string
    def __extract_temperature(self, lines):
        if lines[0].strip()[-3:] == 'YES':
            equals_pos = lines[1].find('t=')
            temp_string = lines[1][equals_pos + 2:]
            return float(temp_string) / 1000.0
        else:
            return float(self.__error_temp)

    # Get all the reported temperatures
    def get_temperatures(self):
        temps = map(self.__extract_temperature, map(self.__read_file_contents, self.__get_input_files()))
        for temp in temps:
            log.info('Read temperature: ' + str(temp))
        return temps

    # Determine if the heating should be turned on according to the passed
    # in temperature
    def check_temperature(self, temperature):
        if temperature == self.__error_temp :
            return False
        elif temperature <= self.__min_temp:
            return True
        elif temperature >= self.__max_temp:
            return False
        else:
            return self.__set_heating_below_max
