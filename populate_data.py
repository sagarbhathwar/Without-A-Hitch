from withoutahitch.models import *

f = open("dummy/User.csv")
lines = list(map(lambda x: x.strip(), f.readlines()))
head = lines[0].split(",")
data = list(map(lambda x: x.split(","), lines[1:]))

for line in data:
    User(**dict(zip(head, line))).save()

f = open("dummy/Vendors.csv")
lines = list(map(lambda x: x.strip(), f.readlines()))
head = lines[0].split(",")
data = list(map(lambda x: x.split(","), lines[1:]))

for line in data:
    Vendor(**dict(zip(head, line))).save()


f = open("dummy/caterer.csv")
lines = list(map(lambda x: x.strip(), f.readlines()))
head = lines[0].split(",")
data = list(map(lambda x: x.split(","), lines[1:]))

for line in data:
    d = dict(zip(head, line))
    vendor = Vendor.objects.get(username=d['vendor'])
    d['vendor'] = vendor
    Caterer(**d).save()


f = open("dummy/venue.csv")
lines = list(map(lambda x: x.strip(), f.readlines()))
head = lines[0].split(",")
data = list(map(lambda x: x.split(","), lines[1:]))

for line in data:
    d = dict(zip(head, line))
    vendor = Vendor.objects.get(username=d['vendor'])
    d['vendor'] = vendor
    Venue(**d).save()

f = open("dummy/decorator.csv")
lines = list(map(lambda x: x.strip(), f.readlines()))
head = lines[0].split(",")
data = list(map(lambda x: x.split(","), lines[1:]))

for line in data:
    d = dict(zip(head, line))
    vendor = Vendor.objects.get(username=d['vendor'])
    d['vendor'] = vendor
    Decorator(**d).save()