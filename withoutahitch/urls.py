from django.conf.urls import url
from . import views


# Useful when referencing views from urls.py
app_name = "withoutahitch"

urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(r"^login/$", views.login_page, name="login_page"),
    url(r"^register/$", views.register_page, name="register_page"),
    url(r"^about/$", views.contact, name="contact"),

    # A page dedicated to each vendor
    url(r"^caterer/(?P<pk>[0-9]+)/$", views.CatererView.as_view(), name='caterer'),
    url(r"^decorator/(?P<pk>[0-9]+)/$", views.DecoratorView.as_view(), name='decorator'),
    url(r"^venue/(?P<pk>[0-9]+)/$", views.VenueView.as_view(), name='venue'),

    # List all vendors
    url(r"^caterers/$", views.Caterers.as_view(), name='caterers'),
    url(r"^decorators/$", views.Decorators.as_view(), name='decorators'),
    url(r"^venues/$", views.Venues.as_view(), name='venues'),

    url(r'^plan/$', views.plan_event, name='plan_event')

]