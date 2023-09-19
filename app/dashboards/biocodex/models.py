# -*- encoding: utf-8 -*-
from app.extensions import db
from sqlalchemy.orm import relationship


class Adress(db.Model):

    __tablename__ = 'adresses'

    id = db.Column(db.Integer, primary_key=True)
    uga = db.Column(db.Text, nullable=False)
    etablissement = db.Column(db.Text)
    adresse = db.Column(db.Text, nullable=False)
    cp = db.Column(db.Text, nullable=False)
    ville = db.Column(db.Text, nullable=False)
    tel = db.Column(db.Text)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    connections = db.relationship("Connections", back_populates="adress")

    def __init__(self, uga, etablissement, adresse, cp, ville):
        self.uga = uga
        self.etablissement = etablissement
        self.adresse = adresse
        self.cp = cp
        self.ville = ville

    def __repr__(self):
        return f'<Lieu: {self.etablissement} {self.adresse} {self.cp} {self.ville} ({self.uga})>'


class Cdb(db.Model):
    __tablename__ = 'cdbs'

    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.Text)
    commentaire = db.Column(db.Text)
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
    ddv = db.Column(db.Integer)

    connections = db.relationship("Connections", back_populates="cdb")


class Identity(db.Model):
    __tablename__ = 'identities'
    __searchable__ = ['nom', 'prenom']

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text, nullable=False)
    prenom = db.Column(db.Text)
    spe = db.Column(db.Text)
    pot = db.Column(db.Integer)
    pvm = db.Column(db.Integer)
    nv2022 = db.Column(db.Integer)
    ciblage = db.Column(db.Integer)

    connections = db.relationship("Connections", back_populates="doc")

    def __repr__(self):
        return f'<Docteur {self.nom} {self.prenom} ({self.spe})>'


class Connections(db.Model):

    __tablename__="connections"

    id = db.Column(db.Integer(), primary_key=True)
    doc_id = db.Column('doc_id', db.ForeignKey('identities.id'), nullable=False)
    adress_id = db.Column('adress_id', db.ForeignKey('adresses.id'), nullable=False)
    cdb_id = db.Column('cdb_id', db.ForeignKey('cdbs.id'), nullable=False)
    doc = db.relationship("Identity", back_populates="connections")
    adress = db.relationship("Adress", back_populates="connections")
    cdb = db.relationship("Cdb", back_populates="connections")
