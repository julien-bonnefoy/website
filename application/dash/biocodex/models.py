# -*- encoding: utf-8 -*-
from application.extensions import db
from geopy.geocoders import Nominatim
import json
from sqlalchemy.types import TypeDecorator, DateTime, String
import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import ARRAY


class Identity(db.Model, SerializerMixin):

    __tablename__ = 'identities'
    __searchable__ = ['nom', 'pre']

    id = db.Column(db.Integer, primary_key=True, unique=True)
    nom = db.Column(db.Text, nullable=False)
    pre = db.Column(db.Text)
    spe1 = db.Column(db.Text)
    spe2 = db.Column(db.Text)
    pot = db.Column(db.Integer)
    pvm = db.Column(db.Integer)
    dec = db.Column(db.Text)
    c24c1 = db.Column(db.Integer)
    c24c2 = db.Column(db.Integer)
    c23c3 = db.Column(db.Integer)
    nv23 = db.Column(db.Integer)
    nv22 = db.Column(db.Integer)
    age = db.Column(db.Integer)
    conv = db.Column(db.Text)
    lieux = db.Column(db.Integer)
    mail = db.Column(db.Text)
    veeva_link = db.Column(db.Text)
    ameli_link = db.Column(db.Text)

    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    connections = db.relationship("Connection", back_populates="doc")
    serialize_rules = ('-connections',)

    def __init__(
            self, nom, pre, spe1, spe2=None, pot=None, pvm=None, dec=None, c24c1=None, c24c2=None, c23c3=None, nv23=None,
            nv22=None, age=None, conv=None, lieux=None, mail=None, veeva_link=None, ameli_link=None
                 ):

        self.nom = nom
        self.pre = pre
        self.spe1 = spe1
        self.spe2 = spe2
        self.pot = pot
        self.pvm = pvm
        self.dec = dec
        self.c24c1 = c24c1
        self.c24c2 = c24c2
        self.c23c3 = c23c3
        self.nv23 = nv23
        self.nv22 = nv22
        self.age = age
        self.conv = conv
        self.lieux = lieux
        self.mail = mail
        self.veeva_link = veeva_link
        self.ameli_link = ameli_link


    def __repr__(self):
        return f'<Docteur {self.nom} {self.pre} ({self.spe1})>'


class Adress(db.Model, SerializerMixin):

    __tablename__ = 'adresses'

    id = db.Column(db.Integer, primary_key=True, unique=True)

    uga = db.Column(db.Text, nullable=False)
    eta = db.Column(db.Text)
    adr = db.Column(db.Text, nullable=False)
    cp = db.Column(db.Text, nullable=False)
    vil = db.Column(db.Text, nullable=False)
    tel = db.Column(db.Text)
    mul = db.Column(db.Text)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    connections = db.relationship("Connection", back_populates="adr")
    serialize_rules = ('-connections', )

    def __init__(self, adr, cp, vil, uga=None, eta=None,  tel=None, mul=None):
        self.uga = uga
        self.eta = eta
        self.adr = adr
        self.cp = cp
        self.vil = vil
        self.tel = tel
        self.mul = mul
        geolocator = Nominatim(user_agent="myBestSecretAgent")
        loc = geolocator.geocode(f"{self.adr} {self.cp} {self.vil}")
        self.lat = loc.latitude
        self.lon = loc.longitude

    def update_eta(self, eta: str, **kwargs):
        self.eta = eta

    def __repr__(self):
        return f'<Lieu: {self.adr} {self.cp} {self.vil} ({self.uga} ({self.lat}, {self.lon})>'


class Cdb(db.Model, SerializerMixin):

    __tablename__ = 'cdbs'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    ddv = db.Column(db.DateTime, nullable=True)
    ddvs = db.Column(ARRAY(db.DateTime))
    rdv = db.Column(db.Text)
    mode = db.Column(db.Text)
    com = db.Column(db.Text)
    rec = db.Column(db.Text)
    motif = db.Column(db.Text)
    lun_m = db.Column(db.Text)
    lun_a = db.Column(db.Text)
    mar_m = db.Column(db.Text)
    mar_a = db.Column(db.Text)
    mer_m = db.Column(db.Text)
    mer_a = db.Column(db.Text)
    jeu_m = db.Column(db.Text)
    jeu_a = db.Column(db.Text)
    ven_m = db.Column(db.Text)
    ven_a = db.Column(db.Text)
    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    connections = db.relationship("Connection", back_populates="cdb")
    serialize_rules = ('-connections',)

    def __init__(self, mode=None, com=None, ddv=None, dpv=None, ddvs=None):
        self.mode = mode
        self.com = com
        self.ddv = ddv
        self.dpv = dpv
        self.ddvs = ddvs


    def save(self):
        ddvs = self.ddvs
        if ddvs is None:
            ddvs = []
        ddv = self.ddv
        if ddv is not None and ddv.strftime("%Y-%m-%d %H:%M:%S") not in ddvs:
            ddvs.append(ddv.strftime("%Y-%m-%d %H:%M:%S"))
        self.ddvs = ddvs
        db.session.commit()
        return "saved"


class Connection(db.Model, SerializerMixin):
    __tablename__ = "connections"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    doc_id = db.Column('doc_id', db.ForeignKey('identities.id'), nullable=False)
    adr_id = db.Column('adr_id', db.ForeignKey('adresses.id'), nullable=False)
    cdb_id = db.Column('cdb_id', db.ForeignKey('cdbs.id'), nullable=False)

    doc = db.relationship("Identity", back_populates="connections")
    adr = db.relationship("Adress", back_populates="connections")
    cdb = db.relationship("Cdb", back_populates="connections")
    serialize_rules = ('-identities', '-adresses', '-cdbs')

    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Pharmacy(db.Model, SerializerMixin):

    __tablename__ = 'pharmacies'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    nom = db.Column(db.Text, nullable=False)
    adr = db.Column(db.Text, nullable=False)
    cp = db.Column(db.Text, nullable=False)
    vil = db.Column(db.Text, nullable=False)
    tel = db.Column(db.Text)
    uga = db.Column(db.Text)
    deco = db.Column(db.Integer)
    c24c1 = db.Column(db.Integer)
    c24c2 = db.Column(db.Integer)
    cib_dp = db.Column(db.Integer)
    cib_dso = db.Column(db.Integer)
    nv22 = db.Column(db.Integer)
    ddv = db.Column(db.DateTime, nullable=True)
    ddvs = db.Column(ARRAY(db.DateTime))
    rdv = db.Column(db.DateTime, nullable=True)
    circ_ca_cma_fev23 = db.Column(db.Float)
    ul_ca_cma_fev23 = db.Column(db.Float)
    ul_ca_rank_fev23 = db.Column(db.Integer)
    circ_ca_cma_juin23 = db.Column(db.Float)
    ul_ca_cma_juin23 = db.Column(db.Float)
    ul_ca_rank_juin23 = db.Column(db.Integer)
    circ_ca_cma_sep23 = db.Column(db.Float)
    ul_ca_cma_sep23 = db.Column(db.Float)
    ul_ca_rank_sep23 = db.Column(db.Integer)
    circ_ca_cma_fev24 = db.Column(db.Float)
    ul_ca_cma_fev24 = db.Column(db.Float)
    ul_ca_rank_fev24 = db.Column(db.Integer)
    gpt = db.Column(db.Text)
    contrat_23 = db.Column(db.Text)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    com = db.Column(db.Text)

    created_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    def __init__(self, id, nom, adr, cp, vil):
        self.id = id
        self.nom = nom
        self.adr = adr
        self.cp = cp
        self.vil = vil
        geolocator = Nominatim(user_agent="myBestSecretAgent")
        loc = geolocator.geocode(f"{self.adr} {self.cp} {self.vil}")
        self.lat = loc.latitude
        self.lon = loc.longitude


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
        return f'<{self.nom}>'


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