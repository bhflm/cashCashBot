import datetime
import logging

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
    with open("last_refresh.txt", "r") as f:
        line = f.read()
        day = line.split(' ')[0]
        return day == today
