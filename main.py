#!/usr/bin/python

# Nikita Kouevda, Eddie Lee, Anthony Sutardja
# 2012/11/10

import random
from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import json

# Flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/test"
db = SQLAlchemy(app)

from models import *

@app.route("/")
def root():
    # TODO

    return "ROOT: Hello, world!"

@app.route("/create_session", methods=["POST"])
def create_session():
    try:
        data = json.loads(request.data)

        session = Session()
        db.session.add(session)

        host = Person(session, data["name"], data["lat"], data["lon"])
        db.session.add(host)

        db.session.commit()

        return jsonify(session_hash=session.session_hash, id=host.id, error=0)
    except Exception as e:
        return jsonify(error=1, msg=str(e))

@app.route("/create_person", methods=["POST"])
def create_person():
    try:
        data = json.loads(request.data)

        session = Session.query.filter_by(session_hash=data["session_hash"]).first()

        if not session:
            raise ValueError

        person = Person(session, data["name"], data["lat"], data["lon"])
        db.session.add(person)

        db.session.commit()

        return jsonify(id=person.id, error=0)
    except:
        return jsonify(error=1)

@app.route("/<session_hash>")
def session(session_hash):
    return "SESSION: hash: %s" % session_hash

@app.route("/<session_hash>/update", methods=["POST"])
def session(session_hash):
    try:
        data = json.loads(request.data)

        session = db.session.query.filter_by(session_hash=session_hash).first()

        if not session:
            raise ValueError

        person = Person.query.filter_by(id=data["id"]).first()
        person.lat = float(data["lat"])
        person.lon = float(data["lon"])

        session.update_center()

        db.session.commit()

        return jsonify(error=0)
    except:
        return jsonify(error=1)

@app.route("/<session_hash>/data", methods=["GET"])
def session(session_hash):
    try:
        session = db.session.query.filter_by(session_hash=session_hash).first()
        persons = [person.json() for person in session.persons]

        return jsonify(persons=persons, center_lat=session.center_lat, center_lon=session.center_lon, dest_lat=session.dest_lat, dest_lon=session.dest_lon, dest_locked=session.dest_locked, error=0)
    except:
        return jsonify(error=1)

@app.route("/<path:path>")
def catch_all(path):
    return "CATCH: path: %s" % path

if __name__ == "__main__":
    app.run(debug=True)
