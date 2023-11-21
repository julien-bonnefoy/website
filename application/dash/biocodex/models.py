# -*- encoding: utf-8 -*-
from application.extensions import db
from geopy.geocoders import Nominatim
from sqlalchemy import inspect
import datetime, time
from sqlalchemy.types import TypeDecorator, DateTime, Integer

import datetime

class TZDateTime(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo:
                raise TypeError("tzinfo is required")
            value = value.astimezone(datetime.timezone.utc).replace(
                tzinfo=None
            )
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value



# SQL Datatype Objects => https://docs.sqlalchemy.org/en/14/core/types.html
class Identity(db.Model):

    __tablename__ = 'identities'
    __searchable__ = ['nom', 'prenom']

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nom = db.Column(db.Text, nullable=False)
    prenom = db.Column(db.Text)
    spe = db.Column(db.Text)
    pot = db.Column(db.Integer)
    pvm = db.Column(db.Integer)
    nv22 = db.Column(db.Integer)
    cib = db.Column(db.Integer)
    dec = db.Column(db.Text)

    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    connections = db.relationship("Connections", back_populates="doc")

    def __init__(self, nom, prenom, spe, pot=None, pvm=None, nv22=None, cib=None, dec=None):
        self.nom = nom
        self.prenom = prenom
        self.spe = spe
        self.pot = pot
        self.pvm = pvm
        self.nv22 = nv22
        self.cib = cib
        self.dec = dec

    # How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f'<Docteur {self.nom} {self.prenom} ({self.spe})>'


class Adress(db.Model):

    __tablename__ = 'adresses'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)

    uga = db.Column(db.Text, nullable=False)
    eta = db.Column(db.Text)
    adr = db.Column(db.Text, nullable=False)
    cp = db.Column(db.Text, nullable=False)
    ville = db.Column(db.Text, nullable=False)
    tel = db.Column(db.Text)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    connections = db.relationship("Connections", back_populates="adr")

    def __init__(self, uga, eta, adr, cp, ville, tel=None):
        self.uga = uga
        self.eta = eta
        self.adr = adr
        self.cp = str(cp)
        self.ville = ville
        self.tel = tel
        geolocator = Nominatim(user_agent="myBestSecretAgent")
        loc = geolocator.geocode(f"{self.adresse} {self.cp} {self.ville}")
        self.lat = loc.latitude
        self.lon = loc.longitude

    def __repr__(self):
        return f'<Lieu: {self.adr} {self.cp} {self.ville} ({self.uga} ({self.lat}, {self.lon})>'


class Cdb(db.Model):

    __tablename__ = 'cdbs'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    mode = db.Column(db.Text)
    com = db.Column(db.Text)
    ddv = db.Column(db.DateTime, nullable=True)
    dpv = db.Column(db.DateTime, nullable=True)
    rdv = db.Column(db.Text)
    rec = db.Column(db.Text)
    pk = db.Column(db.Text)
    lun_mat = db.Column(db.Text)
    lun_am = db.Column(db.Text)
    mar_mat = db.Column(db.Text)
    mar_am = db.Column(db.Text)
    mer_mat = db.Column(db.Text)
    mer_am = db.Column(db.Text)
    jeu_mat = db.Column(db.Text)
    jeu_am = db.Column(db.Text)
    ven_mat = db.Column(db.Text)
    ven_am = db.Column(db.Text)

    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    connections = db.relationship("Connections", back_populates="cdb")


class Connections(db.Model):
    __tablename__ = "connections"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    doc_id = db.Column('doc_id', db.ForeignKey('identities.id'), nullable=False)
    adr_id = db.Column('adr_id', db.ForeignKey('adresses.id'), nullable=False)
    cdb_id = db.Column('cdb_id', db.ForeignKey('cdbs.id'), nullable=False)
    doc = db.relationship("Identity", back_populates="connections")
    adr = db.relationship("Adress", back_populates="connections")
    cdb = db.relationship("Cdb", back_populates="connections")

    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
