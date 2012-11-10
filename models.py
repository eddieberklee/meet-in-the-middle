# Nikita Kouevda, Eddie Lee, Anthony Sutardja
# 2012/11/09

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    persons = db.relationship("Person", backref="session", lazy="dynamic")
    session_hash = db.Column(db.String())
    lat = db.Column(db.Double)
    lon = db.Column(db.Double)

    def __init__(self, persons):
        self.persons = persons
        # TODO hash

    def __repr__(self):
        return "<Session %r>" % self.session_hash

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("session.id"))
    person_hash = db.Column(db.String())
    name = db.Column(db.String())
    lat = db.Column(db.Double)
    lon = db.Column(db.Double)

    def __init__(self, name):
        self.name = name
        # TODO hash

    def __repr__(self):
        return "<Person %r>" % self.person_hash
