import datetime

from project.settings import geolocator


def validate_date_start(date_start):
    today = datetime.date.today()
    if (today.year - datetime.datetime.strptime(date_start, '%Y-%m-%d').date().year) > 2:
        return 'error'
    return date_start


def validate_date_end(date_start, date_end):
    start = datetime.datetime.strptime(date_start, '%Y-%m-%d').date()
    end = datetime.datetime.strptime(date_end, '%Y-%m-%d').date()
    if start > end:
        return 'error'
    return date_end


def validate_from_to(from_to):
    city = geolocator.geocode(from_to)
    if city is None:
        return 'error'
    return from_to


def validate_destiny(destiny):
    city = geolocator.geocode(destiny)
    if city is None:
        return 'error'
    return destiny
