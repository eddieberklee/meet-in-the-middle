# Nikita Kouevda, Eddie Lee, Anthony Sutardja
# 2012/11/10

import random
from string import ascii_letters, digits
from main import db

hash_chars = ascii_letters + digits

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("session.id"))
    session = db.relationship("Session", backref=db.backref("persons", lazy="dynamic"))
    name = db.Column(db.String())
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __init__(self, session, name, lat, lon):
        self.session = session
        self.name = name
        self.lat = lat
        self.lon = lon

    def json(self):
        return {"id": self.id, "name": self.name, "lat": self.lat, "lon": self.lon}

    def __repr__(self):
        return "<Person %r>" % self.id

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_hash = db.Column(db.String())
    center_lat = db.Column(db.Float)
    center_lon = db.Column(db.Float)
    dest_lat = db.Column(db.Float)
    dest_lon = db.Column(db.Float)
    dest_locked = db.Column(db.Boolean)

    def __init__(self, length=5):
        self.session_hash = ''.join(random.choice(hash_chars) for x in range(length))

    def update_center(self):
        self.center_lat = sum(float(person.lat) for person in self.persons) / len(self.persons.all())
        self.center_lon = sum(float(person.lon) for person in self.persons) / len(self.persons.all())

    def set_destination(self, lat=None, lon=None):
        self.dest_lat = lat if lat else self.center_lat
        self.dest_lon = lon if lon else self.center_lon

    def lock_destination(self):
        self.dest_locked = True

    def unlock_destination(self):
        self.dest_locked = False

    def __repr__(self):
        return "<Session %r>" % self.session_hash
