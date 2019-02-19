import datetime
import logging
import os
#Enable logging facilities
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -%(message)s',level=logging.INFO)

def generate_last_refresh_file():
    logging.info('GENERATING LAST REFRESH FILE AT {}'.format(datetime.datetime.now()))
    with open("last_refresh.txt", "w") as f:
        f.write("{}".format(datetime.datetime.now()))


def update_last_refresh_file():
    logging.info('UPDATING REFRESH FILE AT {}'.format(datetime.datetime.now()))
    with open("last_refresh.txt", "w") as f:
        f.write("{}".format(datetime.datetime.now()))


def check_updated_today():
    logging.info('CHECKING IF DATA WAS UPDATED TODAY')
    today = str(datetime.datetime.now()).split(' ')[0]
    today_hour = str(datetime.datetime.now()).split(' ')[1]
    with open("last_refresh.txt", "r") as f:
        line = f.read()
        day = line.split(' ')[0]
        return day == today


def service_healthcheck():
    # checks if service went down i just needed a fancy name
    if (os.path.exists("last_refresh.txt")):
        return check_updated_today()
