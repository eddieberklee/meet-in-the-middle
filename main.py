#!/usr/bin/python

# Nikita Kouevda, Eddie Lee, Anthony Sutardja
# 2012/11/09

import random
from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

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
        session = Session()
        db.session.add(session)

        host = Person(session, request.form["name"], request.form["lat"], request.form["lon"])
        db.session.add(host)

        db.session.commit()

        return jsonify(session.session_hash, host.id, error=0)
    except:
        return jsonify(error=1)

@app.route("/create_person", methods=["POST"])
def create_person():
    try:
        session = Session.query.filter_by(session_hash=request.form["session_hash"]).first()

        if not session:
            raise ValueError

        person = Person(session, request.form["name"], request.form["lat"], request.form["lon"])
        db.session.add(person)

        db.session.commit()

        return jsonify(person.id, error=0)
    except:
        return jsonify(error=1)

@app.route("/<session_hash>")
def session(session_hash):
    return "SESSION: hash: %s" % session_hash

@app.route("/<session_hash>/update", methods=["POST"])
def session(session_hash):
    try:
        session = db.session.query.filter_by(session_hash=session_hash).first()

        if not session:
            raise ValueError

        person = Person.query.filter_by(id=request.form["id"]).first()
        person.lat = float(request.form["lat"])
        person.lon = float(request.form["lon"])

        session.update_center()

        db.session.commit()

        return jsonify(error=0)
    except:
        return jsonify(error=1)

@app.route("/<session_hash>/data", methods=["POST"])
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
    app.run()
