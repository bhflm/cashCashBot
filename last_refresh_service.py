from datetime import datetime, timedelta
import logging
import os
#Enable logging facilities
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -%(message)s',level=logging.INFO)

def generate_last_refresh_file():
    logging.info('GENERATING LAST REFRESH FILE AT {}'.format(datetime.now()))
    with open("last_refresh.txt", "w") as f:
        f.write("{}".format(datetime.now()))


def update_last_refresh_file():
    logging.info('UPDATING REFRESH FILE AT {}'.format(datetime.now()))
    with open("last_refresh.txt", "w") as f:
        f.write("{}".format(datetime.now()))


def get_last_refresh():
    with open("last_refresh.txt", "r") as f:
        line = f.read()
        return line

def check_updated_today():
    logging.info('CHECKING IF DATA WAS UPDATED TODAY')
    today = str(datetime.now()).split(' ')[0]
    today_hour = str(datetime.now()).split(' ')[1]
    with open("last_refresh.txt", "r") as f:
        line = f.read()
        day = line.split(' ')[0]
        return day == today


def days_between(d1, d2):
    print(d1)
    print(d2)
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d1 - d1).days)

def format_date(date):
    return str(get_last_refresh().split(' ')[0]) + ' ' + str(get_last_refresh().split(' ')[1])[:7]

def is_weekend(weekday):
    return weekday == 6 or weekday == 5

def check_last_refresh():
    logging.info('CHECKING LAST REFRESH ON ATMS')
    now = datetime.now()
    last_refresh = datetime.strptime(get_last_refresh(), '%Y-%m-%d %H:%M:%S.%f')
    hours_difference = int(str(now - last_refresh).split(':')[0])
    #  where Monday is 0 and Sunday is 6
    weekday = datetime.date(now).weekday()

    return (hours_difference >= 8 and not is_weekend(weekday))


def service_healthcheck():
    # checks if service went down i just needed a fancy name
    if (os.path.exists("last_refresh.txt")):
        return check_updated_today()
