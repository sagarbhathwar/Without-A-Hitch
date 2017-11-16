import os

files = ['User.json', 'Vendor.json', 'Service.json', 'Venue.json',
         'Decorator.json', 'Caterer.json', 'Event.json', 'Marriage.json',
         'Conference.json', 'Meeting.json', 'Cuisine.json']

for file in files:
    os.system("python manage.py dummy/" + file)

