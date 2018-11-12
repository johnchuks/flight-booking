import datetime
import time


def convert_date_to_unix(date):
    return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
