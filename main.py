#!/usr/bin/python

# Nikita Kouevda, Eddie Lee, Anthony Sutardja
# 2012/11/10

import random
from flask import Flask, request, jsonify, render_template
import json, yelp
from flask.ext.sqlalchemy import SQLAlchemy
import os

# Flask
app = Flask(__name__)

db_server_url = os.environ.get('DATABASE_URL', "postgresql://localhost/test")
app.config["SQLALCHEMY_DATABASE_URI"] = db_server_url
db = SQLAlchemy(app)

from models import *

@app.route("/")
def root():
    return render_template('splash.html')

@app.route("/host")
def host():
    return render_template('host.html')

@app.route("/create_session", methods=["POST"])
def create_session():
    try:
        #print request.data
        #data = json.loads(request.data)
        data = request.form

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
        #data = json.loads(request.data)
        data = request.form

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
    return render_template('main.html')

@app.route("/<session_hash>/update", methods=["POST"])
def session_update(session_hash):
    try:
        #data = json.loads(request.data)
        data = request.form

        session = Session.query.filter_by(session_hash=session_hash).first()

        if not session:
            raise ValueError

        person =  Person.query.filter_by(id=int(data["id"])).first()
        person.lat = float(data["lat"])
        person.lon = float(data["lon"])

        session.update_center()

        db.session.commit()

        return jsonify(error=0)
    except:
        return jsonify(error=1)

@app.route("/session/places", methods=["GET"])
def places():
    try:
				places = yelp.places()
				return jsonify(places=places, error=0)
    except:
        return jsonify(error=1)

@app.route("/<session_hash>/places", methods=["GET"])
def session_places(session_hash):
    try:
        session = Session.query.filter_by(session_hash=session_hash).first()

        if session.dest_locked:
            places = yelp.places(point=str(session.dest_lat)+str(session.dest_lon))
        else:
            places = yelp.places(point=str(session.center_lat)+str(session.center_lon))

        return jsonify(places=places, error=0)
    except:
        return jsonify(error=1)

@app.route("/<session_hash>/data", methods=["GET"])
def session_data(session_hash):
    try:
        session = Session.query.filter_by(session_hash=session_hash).first()
        persons = [person.json() for person in session.persons]

        return jsonify(persons=persons, center_lat=session.center_lat, center_lon=session.center_lon, dest_lat=session.dest_lat, dest_lon=session.dest_lon, dest_locked=session.dest_locked, error=0)
    except:
        return jsonify(error=1)

@app.route("/<path:path>")
def catch_all(path):
    return "CATCH: path: %s" % path

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
