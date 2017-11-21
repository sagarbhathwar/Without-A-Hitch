import sys
import random

from django import forms
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
import psycopg2
import psycopg2.extras

from .models import *
from .forms import NameForm

EVENT_TYPES = [subclass.__name__ for subclass in Event.__subclasses__()]
SERVICE_TYPES = [subclass.__name__ for subclass in Service.__subclasses__()]

# view for handling registering event.
def registering_user(request):
    # needs to be implemented, ez in 5 min
    print("dummy print to rectify identation prob") 

def login_page(request):
    return render(request, template_name="withoutahitch/login.html")


def register_page(request):
    return render(request, template_name="withoutahitch/register.html")


def contact(request):
    return render(request, template_name="withoutahitch/contact.html")


# view when a user presses the logout button provided on the page
def logging_out(request):
    try:
        # deletes the session  
        del request.session['username']
    except:
        pass
    # returns back to login page.
    return render(request,template_name="withoutahitch/login.html")

def auth(request):
    # get the user name and password.
    user_name = request.POST.get('username', '')
    # get the password
    password = request.POST.get('password', '')
    # connect to a database
    try:
        # connceting to a withoutahitch database.
        conn = psycopg2.connect("dbname = 'withoutahitch' user = 'team7' host = 'localhost' password = 'password'")
    except:
        print("Unable to connect to the database")
    cursor = conn.cursor()
    user_valid = True
    pass_valid = True
    # check if user exists.
    SQL = "SELECT * FROM withoutahitch_user where username = %s;"
    data = (user_name,)
    cursor.execute(SQL, data)
    records = cursor.fetchall()
    print(records)
    if (not len(records)):
        # return error saying user doesn't exist
        user_valid = False
        print("User doesn't exist")  # prints on the STDOUT
    # if then get the password for that particular user and check against the password entered.
    SQL = "SELECT password from withoutahitch_user WHERE username = %s;"
    data = (user_name,)
    cursor.execute(SQL, data)
    records = cursor.fetchall()
    for i in records:
        if (i[0] == password):
            print("User exists and password given is valid")
        else:
            pass_valid = False
    if (user_valid and pass_valid):
        # return along with the proper page a session kind of variable
        # The first argument i.e request contains a dictionary like session variabe in it.
        # Assigning a session variable , needs to be used in every page where the user uses it.
        request.session['username'] = user_name
        return render(request, {"username" : session_name},template_name="withoutahitch/success.html")
    else:
        # return render(request, template_name = "withoutahitch/login.html")
        # the kwargs argument is used to send form which has forms.error and can be used to display
        # the message when the log in fails.
        return HttpResponseRedirect(reverse('withoutahitch:login_page',kwargs = {'form':forms.Form}))


class IndexView(generic.ListView):
    template_name = "withoutahitch/index.html"
    context_object_name = "latest_events"

    def get_queryset(self):
        return Event.objects.order_by("-date")[:5]


class Venues(generic.ListView):
    template_name = "withoutahitch/venues.html"
    context_object_name = "venues"

    def get_queryset(self):
        return Venue.objects.all()


class Decorators(generic.ListView):
    template_name = "withoutahitch/decorators.html"
    context_object_name = "decorators"

    def get_queryset(self):
        return Decorator.objects.all()


class Caterers(generic.ListView):
    template_name = "withoutahitch/caterers.html"
    context_object_name = "caterers"

    def get_queryset(self):
        return Caterer.objects.all()


class VenueView(generic.DetailView):
    template_name = "withoutahitch/venue.html"
    model = Venue


class CatererView(generic.DetailView):
    template_name = "withoutahitch/caterer.html"
    model = Caterer


class DecoratorView(generic.DetailView):
    template_name = "withoutahitch/decorator.html"
    model = Decorator


def pick_your_own(request):
    decorators = Decorator.objects.all()
    venues = Venue.objects.all()
    caterers = Caterer.objects.all()

    return render(request, "withoutahitch/pick_your_own.html",
                  context={"decorators": decorators,
                           "venues": venues,
                           "caterers": caterers,
                           "event_types": EVENT_TYPES
                           })


def pick_package(request):
    package1 = 0
    return render(request, "withoutahitch/pick_package.html")


def plan_event(request):
    return render(request, "withoutahitch/plan.html")


def book_event(request):
    event_type = request.GET['event_type']
    venue = Venue.objects.get(pk=request.GET['venue'])
    caterer = Caterer.objects.get(pk=request.GET['caterer'])
    decorator = Decorator.objects.get(pk=request.GET['decorator'])
    date = request.GET['event_date']

    total_cost = venue.cost + caterer.cost + decorator.cost
    budget = 1.1 * total_cost

    # For now, it is assigned to a random user
    users = User.objects.all()
    user = users[random.randint(0, len(users)) - 1]

    caterer_availability = CatererAvailability(caterer=caterer, allocated_date=date)
    venue_availability = VenueAvailability(venue=venue, allocated_date=date)

    try:
        venue_availability.save()
    except IntegrityError:
        messages.error(request, 'Venue is not available for the selected date')

    else:
        try:
            caterer_availability.save()
        except IntegrityError:
            print("Error occured")
            messages.error(request, 'Caterer is not available for the selected date')

        else:
            Event_ = getattr(sys.modules[__name__], event_type)
            evt = Event_(date=date, venue=venue, caterer=caterer, decorator=decorator, user=user, budget=budget)
            evt.save()
            messages.info(request, 'Event booked successfully')

    return HttpResponseRedirect(reverse("withoutahitch:plan_event"))
