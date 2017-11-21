from django.conf.urls import url
from . import views
import django

# Useful when referencing views from urls.py
app_name = "withoutahitch"

urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(r"^login/$", views.login_page, name="login_page"),
    url(r"^register/$", views.register_page, name="register_page"),
    url(r"^about/$", views.contact, name="contact"),
    url(r"^logging/$" , views.auth, name = "logging"),
    # adding logout for future use.
    url(r"^loggingout",views.logging_out,name = "logging_out"),
    # adding the view when a user presses register button.
    url(r"^registering",views.registering_user , name = "registering_user"),

    # A page dedicated to each vendor
    url(r"^caterer/(?P<pk>[0-9]+)/$", views.CatererView.as_view(), name='caterer'),
    url(r"^decorator/(?P<pk>[0-9]+)/$", views.DecoratorView.as_view(), name='decorator'),
    url(r"^venue/(?P<pk>[0-9]+)/$", views.VenueView.as_view(), name='venue'),

    # List all vendors
    url(r"^caterers/$", views.Caterers.as_view(), name='caterers'),
    url(r"^decorators/$", views.Decorators.as_view(), name='decorators'),
    url(r"^venues/$", views.Venues.as_view(), name='venues'),

    # Plan: Includes pick your own, package etc.
    url(r'^plan/$', views.plan_event, name='plan_event'),
    url(r'^pick_your_own/$', views.pick_your_own, name='pick_your_own'),
    url(r'^pick_package/$', views.pick_package, name='pick_package'),

    url(r'^book_event/$', views.book_event, name='book_event')
]