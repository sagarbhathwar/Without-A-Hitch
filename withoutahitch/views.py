import random
import sys

import psycopg2
import psycopg2.extras
from django import forms
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from .models import *

EVENT_TYPES = [subclass.__name__ for subclass in Event.__subclasses__()]
SERVICE_TYPES = [subclass.__name__ for subclass in Service.__subclasses__()]


def check_username(request, username):
    return User.objects.filter(username__iexact=username).exists()


# view for handling registering event.
def registering_user(request):
    username = request.POST['username']
    name = request.POST['name']
    email_id = request.POST['email']
    contact_num = request.POST['contact']
    address = request.POST['address']
    password = request.POST['password']

    if User.objects.filter(username__iexact=username).exists():
        messages.error(request, "Username is taken")
        return HttpResponseRedirect(reverse('withoutahitch:register_page'))
    if User.objects.filter(email_id__iexact=email_id):
        messages.error(request, "Email is taken")
        return HttpResponseRedirect(reverse('withoutahitch:register_page'))
    if User.objects.filter(contact_num__iexact=contact_num):
        messages.error(request, "Contact number already exists")
        return HttpResponseRedirect(reverse('withoutahitch:register_page'))

    else:
        User(username=username, name=name, email_id=email_id,
             contact_num=contact_num, address=address, password=password).save()
        messages.info(request, "Registered successfully")
        return render(request, template_name="withoutahitch/login.html")


def base_page(request):
    return render(request, template_name="withoutahitch/base.html")


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
    return render(request, template_name="withoutahitch/login.html")


def auth(request):
    # get the user name and password.
    user_name = request.POST['username']
    # get the password
    password = request.POST['password']
    # Assign a dummy session variable.
    session_name = 'no user logged in'
    # above session name can be initialized to request.session['username'] and
    # can be used if a person without logging in tries to view any html page.
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
        if i[0] == password:
            print("User exists and password given is valid")
        else:
            pass_valid = False
    if user_valid and pass_valid:
        # return along with the proper page a session kind of variable
        # The first argument i.e request contains a dictionary like session variabe in it.
        # Assigning a session variable , needs to be used in every page where the user uses it.
        request.session['username'] = user_name
        session_name = user_name
        request.session['username'] = session_name
        return render(request, "withoutahitch/index.html", context={"username": session_name})
    else:
        return HttpResponseRedirect(reverse('withoutahitch:login_page', kwargs={'form': forms.Form}))


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
    try:
        username = request.session.username
    except AttributeError:
        messages.error(request, "Login before booking an event")

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
    try:
        user = request.session.username
    except AttributeError:
        redirect('withoutahitch:login_page')

    else:

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
