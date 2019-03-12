from django.contrib.postgres.fields import ArrayField
from django.db import models
from geopy.distance import geodesic
from rest_framework.generics import get_object_or_404

from project.settings import geolocator
from trips.validators import validate_date_start, validate_date_end, validate_from_to, validate_destiny
from users.models import User


class Trip(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    mates = ArrayField(models.IntegerField(), default=list)
    destiny = models.CharField(max_length=100)
    from_to = models.CharField(max_length=100)
    pictures = ArrayField(models.URLField(blank=True, null=True), default=list, size=8, blank=True)
    verified = models.BooleanField(default=False)
    counter_verified = models.IntegerField(default=0)
    kms = models.IntegerField()
    route = models.TextField(blank=True)
    views = models.IntegerField(default=0)
    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)
    #TODO: add create_at to make order_by last created on top

    @staticmethod
    def create_trip(obj , user):
        trip = Trip()
        trip.owner = user
        date_start = validate_date_start(obj.get('date_start'))
        if date_start == 'error':
            response = 'Can\'t publish trips older than 2 years'
            return response
        trip.date_start = date_start
        date_end = validate_date_end(date_start=date_start, date_end=obj.get('date_end'))
        if date_end == 'error':
            response = 'Date start can\'t be greater that Date end'
            return response
        trip.date_end = date_end
        from_to = validate_from_to(obj.get('from_to'))
        if from_to  == 'error':
            response = 'City from_to can\'t be found'
            return response
        trip.from_to = from_to
        destiny = validate_destiny(obj.get('destiny'))
        if destiny == 'error':
            response = 'City destiny can\'t be found'
            return response
        trip.destiny = destiny
        trip.kms = Trip.calculate_kms_between_cities(
            from_to=trip.from_to, destiny=trip.destiny
        )
        trip.route = obj.get('route')
        trip.verified = False
        trip.counter_verified = 0
        trip.views = 0
        trip.save()
        return trip

    @staticmethod
    def calculate_kms_between_cities(from_to, destiny):
        location_one = geolocator.geocode(from_to)
        location_two = geolocator.geocode(destiny)
        location_from = (location_one.latitude, location_one.longitude)
        location_destiny = (location_two.latitude, location_two.longitude)
        return geodesic(location_from, location_destiny).km

    @staticmethod
    def new_visit(trip):
        new_visit = 1
        trip.views = trip.views + new_visit
        trip.save()
