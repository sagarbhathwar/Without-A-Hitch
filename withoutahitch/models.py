import abc

from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    email_id = models.EmailField(unique=True)
    contact_num = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=200)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    contact_num = models.CharField(max_length=50)
    email_id = models.EmailField()

    def __str__(self):
        return self.name


class Service(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    contact_num = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField()
    cost = models.IntegerField()

    def __str__(self):
        return self.name


class Venue(Service):
    venue_size = models.IntegerField()


class Decorator(Service):
    pass


class Caterer(Service):
    pass


class Event(models.Model):
    date = models.DateTimeField()
    booking_date = models.DateField(default=timezone.now)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    caterer = models.ForeignKey(Caterer, on_delete=models.CASCADE)
    decorator = models.ForeignKey(Decorator, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.IntegerField()

    @abc.abstractmethod
    def __str__(self):
        return

    class Meta:
        unique_together = (('date', 'caterer'), ('date','venue'))


class Marriage(Event):
    pass

    def __str__(self):
        return "Marriage at " + str(Venue) + " on " + str(self.date)


class Conference(Event):
    pass

    def __str__(self):
        return "Conference at " + str(Venue) + " on " + str(self.date)


class Meeting(Event):
    pass

    def __str__(self):
        return "Meeting at " + str(Venue) + " on " + str(self.date)


class CustomEvent(Event):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " at " + str(Venue) + " on " + str(self.date)


class Cuisine(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField()


class CatererCuisine(models.Model):
    caterer = models.OneToOneField(Caterer, on_delete=models.CASCADE)
    cuisine = models.OneToOneField(Cuisine, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("caterer", "cuisine")


class VenueAvailability(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    allocated_date = models.DateField()

    class Meta:
        unique_together = ("venue", "allocated_date")


class CatererAvailability(models.Model):
    caterer = models.ForeignKey(Caterer, on_delete=models.CASCADE)
    allocated_date = models.DateField()

    class Meta:
        unique_together = ("caterer", "allocated_date")
