# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime

from analysis.database import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


class Address(db.Model):
    UDPRN = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50))
    Address1 = db.Column(db.String(50))
    Address2 = db.Column(db.String(50))
    Address3 = db.Column(db.String(50))
    Address4 = db.Column(db.String(50))
    Address5 = db.Column(db.String(50))
    Address6 = db.Column(db.String(50))
    Address7 = db.Column(db.String(50))
    Address8 = db.Column(db.String(50))
    Address9 = db.Column(db.String(50))
    Address10 = db.Column(db.String(50))
    Postcode = db.Column(db.String(50))
    Created = db.Column(db.DateTime)

    def __init__(self, udprn, postcode, name="", address1="", address2="",  address3="", address4="", address5="", address6="", address7="", address8="", address9="", address10="", created=datetime.utcnow()):
        self.Postcode = postcode
        self.UDPRN = udprn
        self.Name = name
        self.Address1 = address1
        self.Address2 = address2
        self.Address3 = address3
        self.Address4 = address4
        self.Address5 = address5
        self.Address6 = address6
        self.Address7 = address7
        self.Address8 = address8
        self.Address9 = address9
        self.Address10 = address10
        self.Created = created

    def __repr__(self):
        return '<Address %r>' % self.Postcode
