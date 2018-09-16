from HeatingController import HeatingController
from Scheduler import Scheduler
from TemperatureMonitor import TemperatureMonitor

# Temp at which to turn heating off
MAX_TEMP = 55
# Temp at which to turn heating on
MIN_TEMP = 40
# Error value when temp cannot be read
ERROR_TEMP = -999
# Should the heating be on between min && max temp?
SET_HEATING_ON_BELOW_MAX = True
# The channels of the output pins
GPIO_OUTPUT_UPSTAIRS = 17
GPIO_OUTPUT_DOWNSTAIRS = 18


def main():
    temp_mon = TemperatureMonitor(
        error_temp=ERROR_TEMP,
        min_temp=MIN_TEMP,
        max_temp=MAX_TEMP,
        set_heating_below_max=SET_HEATING_ON_BELOW_MAX)
    heating_controller = HeatingController(
        gpio_output_downstairs=GPIO_OUTPUT_DOWNSTAIRS,
        gpio_output_upstairs=GPIO_OUTPUT_UPSTAIRS, temp_monitor=temp_mon)
    scheduler = Scheduler(heating_controller=heating_controller)
    scheduler.start()


if __name__ == "__main__":
    main()
