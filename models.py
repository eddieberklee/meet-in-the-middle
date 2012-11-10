# Nikita Kouevda, Eddie Lee, Anthony Sutardja
# 2012/11/09

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

    def __repr__(self):
        return "<Person %r>" % self.person_hash

    def json(self):
        return {"id": self.id, "name": self.name, "lat": self.lat, "lon": self.lon}

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_hash = db.Column(db.String())
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __init__(self):
        self.session_hash = ''.join(random.choice(hash_chars) for x in range(length))

    def __repr__(self):
        return "<Session %r>" % self.session_hash
