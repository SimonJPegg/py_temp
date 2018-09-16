import time
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:

    def __init__(self, heating_controller):
        self.__heating_controller = heating_controller

    # Setup the heating schedule and launch the scheduler
    def start(self):
        # On for 10 mins off for 5 (downstairs for 3 mins)
        # if between 6am and 10am turn on upstairs
        # 10am and 8pm turn on downstairs
        # 8pm and 6 am turn on both
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.__heating_controller.set_heating_upstairs, 'cron', hour='0-6', minute='1-59/15')
        scheduler.add_job(self.__heating_controller.set_heating_downstairs, 'cron', hour='0-6', minute='1-59/13')
        scheduler.add_job(self.__heating_controller.set_heating_upstairs, 'cron', hour='6-10', minute='1-59/15')
        scheduler.add_job(self.__heating_controller.set_heating_downstairs, 'cron', hour='10-20', minute='1-59/13')
        scheduler.add_job(self.__heating_controller.set_heating_upstairs, 'cron', hour='20-23', minute='1-59/15')
        scheduler.add_job(self.__heating_controller.set_heating_downstairs, 'cron', hour='20-23', minute='1-59/13')
        scheduler.start()

        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        while True:
            try:
                # This is here to simulate application activity (which keeps the main thread alive).
                time.sleep(2)
            except (KeyboardInterrupt, SystemExit):
                # Not strictly necessary if daemonic mode is enabled but should be done if possible
                scheduler.shutdown()
