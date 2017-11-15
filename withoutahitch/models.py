import abc

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    email_id = models.EmailField(unique=True)
    contact_num = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=200)
    password = models.CharField(max_length = 50,default = 'password')
    
    def __str__(self):
        return self.name


class Vendor(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    contact_num = models.CharField(max_length=50)
    email_id = models.EmailField()


class Service(models.Model):
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
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
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)
    caterer_id = models.ForeignKey(Caterer, on_delete=models.CASCADE)
    decorater_id = models.ForeignKey(Decorator, on_delete=models.CASCADE)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.IntegerField()

    @abc.abstractmethod
    def __str__(self):
        return


class Marriage(Event):
    pass

    def __str__(self):
        return "Marriage at " + str(Venue.objects.get(pk=self.venue_id)) + " on " + str(self.date)


class Conference(Event):
    pass

    def __str__(self):
        return "Conference at " + str(Venue.objects.get(pk=self.venue_id)) + " on " + str(self.date)


class Meeting(Event):
    pass

    def __str__(self):
        return "Meeting at " + str(Venue.objects.get(pk=self.venue_id)) + " on " + str(self.date)


class CustomEvent(Event):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " at " + str(Venue.objects.get(pk=self.venue_id)) + " on " + str(self.date)


class Cuisine(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.ImageField()


class CatererCuisine(models.Model):
    caterer_id = models.OneToOneField(Caterer, on_delete=models.CASCADE, primary_key=True)
    cuisine_id = models.OneToOneField(Cuisine, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("caterer_id", "cuisine_id")


class EventService(models.Model):
    event_id = models.OneToOneField(Event, on_delete=models.CASCADE, primary_key=True)
    service_id = models.OneToOneField(Service, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("event_id", "service_id")


class VenueAvailability(models.Model):
    venue_id = models.OneToOneField(Venue, on_delete=models.CASCADE, primary_key=True)
    allocated_date = models.DateField()

    class Meta:
        unique_together = ("venue_id", "allocated_date")


class CatererAvailability(models.Model):
    caterer_id = models.OneToOneField(Caterer, on_delete=models.CASCADE, primary_key=True)
    allocated_date = models.DateField()

    class Meta:
        unique_together = ("caterer_id", "allocated_date")
