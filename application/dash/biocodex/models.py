# -*- encoding: utf-8 -*-
from application.extensions import db
from geopy.geocoders import Nominatim
from sqlalchemy import inspect
import json
from sqlalchemy.types import TypeDecorator, DateTime, Integer, String

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

class Json(TypeDecorator):

    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

# SQL Datatype Objects => https://docs.sqlalchemy.org/en/14/core/types.html
class Identity(db.Model):

    __tablename__ = 'identities'
    __searchable__ = ['nom', 'prenom']

    id = db.Column(db.Integer, primary_key=True, unique=True)
    titre = db.Column(db.Text)
    nom = db.Column(db.Text, nullable=False)
    prenom = db.Column(db.Text)
    spe = db.Column(db.Text)
    tend = db.Column(db.Text)
    pot = db.Column(db.Integer)
    pvm = db.Column(db.Integer)
    nv22 = db.Column(db.Integer)
    cib = db.Column(db.Integer)
    dec = db.Column(db.Text)
    mix = db.Column(db.Text)
    dip = db.Column(db.Integer)
    nais = db.Column(db.Integer)
    mail = db.Column(db.Text)

    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    connections = db.relationship("Connections", back_populates="doc")

    def __init__(self, nom, prenom,  spe, titre=None, tend=None, pot=None, pvm=None, nv22=None, cib=None, dec=None, mix=None, dip=None, nais=None, mail=None):
        self.titre = titre
        self.nom = nom
        self.prenom = prenom
        self.spe = spe
        self.tend = tend
        self.pot = pot
        self.pvm = pvm
        self.nv22 = nv22
        self.cib = cib
        self.dec = dec
        self.mix = mix
        self.dip = dip
        self.nais = nais
        self.mail = mail

    # How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f'<Docteur {self.nom} {self.prenom} ({self.spe})>'


class Adress(db.Model):

    __tablename__ = 'adresses'

    id = db.Column(db.Integer, primary_key=True, unique=True)

    uga = db.Column(db.Text, nullable=False)
    eta = db.Column(db.Text)
    adr = db.Column(db.Text, nullable=False)
    cp = db.Column(db.Text, nullable=False)
    ville = db.Column(db.Text, nullable=False)
    tel = db.Column(db.Text)
    par1 = db.Column(db.Text)
    par2 = db.Column(db.Text)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    connections = db.relationship("Connections", back_populates="adr")

    def __init__(self, adr, cp, ville, uga=None, eta=None,  tel=None, par1=None, par2=None):
        self.uga = uga
        self.eta = eta
        self.adr = adr
        self.cp = str(cp)
        self.ville = ville
        self.tel = tel
        self.par1 = par1
        self.par2 = par2
        geolocator = Nominatim(user_agent="myBestSecretAgent")
        loc = geolocator.geocode(f"{self.adr} {self.cp} {self.ville}")
        self.lat = loc.latitude
        self.lon = loc.longitude

    def __repr__(self):
        return f'<Lieu: {self.adr} {self.cp} {self.ville} ({self.uga} ({self.lat}, {self.lon})>'


class Cdb(db.Model):

    __tablename__ = 'cdbs'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    mode = db.Column(db.Text)
    com = db.Column(db.Text)
    ddv = db.Column(db.DateTime, nullable=True)
    ddvs = db.Column(db.ARRAY(db.Text))
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

    def __init__(self, mode=None, com=None, ddv=None, dpv=None):
        self.mode = mode
        self.com = com
        self.ddv = ddv
        self.dpv = dpv


    def save(self):
        ddvs = self.ddvs
        if ddvs is None:
            ddvs = []
        ddv = self.ddv
        if ddv is not None and ddv.strftime("%Y-%m-%d %H:%M:%S") not in ddvs:
            ddvs.append(ddv.strftime("%Y-%m-%d %H:%M:%S"))
        self.ddvs = ddvs
        db.session.commit()
        return ddvs



class Connections(db.Model):
    __tablename__ = "connections"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    doc_id = db.Column('doc_id', db.ForeignKey('identities.id'), nullable=False)
    adr_id = db.Column('adr_id', db.ForeignKey('adresses.id'), nullable=False)
    cdb_id = db.Column('cdb_id', db.ForeignKey('cdbs.id'), nullable=False)
    doc = db.relationship("Identity", back_populates="connections")
    adr = db.relationship("Adress", back_populates="connections")
    cdb = db.relationship("Cdb", back_populates="connections")

    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())




class Pharmacy(db.Model):

    __tablename__ = 'pharmacies'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    nom = db.Column(db.Text, nullable=False)
    cip = db.Column(db.Integer)
    adr = db.Column(db.Text, nullable=False)
    cp = db.Column(db.Text, nullable=False)
    ville = db.Column(db.Text, nullable=False)
    tel = db.Column(db.Text)
    uga = db.Column(db.Text, nullable=False)
    cib_vm = db.Column(db.Text)
    cib_dp = db.Column(db.Text)
    cib_dso = db.Column(db.Text)
    nv22 = db.Column(db.Text)
    ddv = db.Column(db.DateTime, nullable=True)
    ddvs = db.Column(db.ARRAY(db.Text))
    rdv = db.Column(db.DateTime, nullable=True)
    ca_circ_cma_fev23 = db.Column(db.Text)
    rang_ca_circ_fev23 = db.Column(db.Text)
    ca_ul_cma_fev_23 = db.Column(db.Text)
    rang_ca_ul_fev23 = db.Column(db.Text)
    ca_circ_cma_juin23 = db.Column(db.Text)
    rang_ca_circ_juin23 = db.Column(db.Text)
    ca_ul_cma_juin_23 = db.Column(db.Text)
    rang_ca_ul_juin23 = db.Column(db.Text)
    ca_circ_cma_sept23 = db.Column(db.Text)
    ca_ul_cma_sept23 = db.Column(db.Text)
    rang_ca_ul_sept23 = db.Column(db.Text)
    decil_23 = db.Column(db.Text)
    groupement = db.Column(db.Text)
    contrat_23 = db.Column(db.Text)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    com = db.Column(db.Text)

    def __init__(self, id, nom, cip, adr, cp, ville):
        self.id = id
        self.nom = nom
        self.cip = cip
        self.adr = adr
        self.cp = cp
        self.ville = ville
        geolocator = Nominatim(user_agent="myBestSecretAgent")
        loc = geolocator.geocode(f"{self.adr} {self.cp} {self.ville}")
        self.lat = loc.latitude
        self.lon = loc.longitude

    # How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def save(self):
        ddvs = self.ddvs
        if ddvs is None:
            ddvs = []
        ddv = self.ddv
        if ddv is not None and ddv.strftime("%Y-%m-%d %H:%M:%S") not in ddvs:
            ddvs.append(ddv.strftime("%Y-%m-%d %H:%M:%S"))
        self.ddvs = ddvs
        db.session.commit()
        return ddvs

    def __repr__(self):
        return f'<{self.nom} ({self.cip})>'