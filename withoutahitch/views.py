from django.shortcuts import render
from django.views import generic

from .models import *


def login_page(request):
    return render(request, template_name="withoutahitch/login.html")


def register_page(request):
    return render(request, template_name="withoutahitch/register.html")


def contact(request):
    return render(request, template_name="withoutahitch/contact.html")


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


def plan_event(request):
    decorators = Decorator.objects.all()
    venues = Decorator.objects.all()
    caterers = Caterer.objects.all()

    return render(request, "withoutahitch/plan.html",
                  context={"decorators": decorators,
                           "venues": venues,
                           "caterers": caterers
                           })

