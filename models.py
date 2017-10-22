from django.db import models

# Create your models here.
class User(models.Model):	
	name = models.CharField(max_length=50, unique=True)
	emailid = models.EmailField()
	contactnum = models.CharField(max_length=50)
	address = models.CharField(max_length=200)

class CustomEvent(models.Model):
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)

class Event(models.Model):
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)
	caterer_id = models.ForeignKey(Caterer, on_delete=models.CASCADE)
	decorater_id = models.ForeignKey(Decorater, on_delete=models.CASCADE)
	vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	budget = models.IntegerField()

class Marriage(models.Model):
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)

class Conference(models.Model):
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)

class Meeting(models.Model):
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)

class Venue(models.Model):
	service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
	venuesize = models.IntegerField()

class Decorator(models.Model):
	service_id = models.ForeignKey(Service, on_delete=models.CASCADE)

class Caterer(models.Model):
	service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
	
class Cuisine(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=100)
	image = models.ImageField()

class CatererCuisine(models.Model):
	cuisine_id = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
	caterer_id = models.ForeignKey(Caterer, on_delete=models.CASCADE)

class Service(models.Model):
	vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	contactnum = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	description = models.CharField(max_length=100)
	image = models.ImageField()

class EventService(models.Model):
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	service_id = models.ForeignKey(Service, on_delete=models.CASCADE)

class Vendor(models.Model):
	contactnum = models.CharField(max_length=50)
	emailid = models.EmailField()

class VenueAvailability(models.Model):
	venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)
	allocated_date = models.DateField()

class CatererAvailability(models.Model):
	caterer_id = models.ForeignKey(Caterer, on_delete=models.CASCADE)
	allocated_date = models.DateField()
