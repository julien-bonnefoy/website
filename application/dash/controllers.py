from flask import request, jsonify, flash, redirect
from application.dash.biocodex.models import Identity, Pharmacy
import pandas as pd
from application.config import basedir, config
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import create_engine
import os
from application import db

load_dotenv(os.path.join(basedir, '.env'))
DATABASE_URL = f'postgresql://{os.environ.get("USERNAME")}:{os.environ.get("PASSWORD")}@{os.environ.get("HOST")}:{os.environ.get("PORT")}/{os.environ.get("DATABASE")}'

# an Engine, which the Session will use for connection
# resources
engine = create_engine(DATABASE_URL)

# Query Object Methods => https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query
# Session Object Methods => https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522

def list_all_pds_ctrlr():
    pdss = Identity.query.all()
    response = []
    for pds in pdss:
        response.append(pds.toDict())
    return jsonify(response)


def create_pds_ctrlr():
    request_form = request.form.to_dict()

    new_pds = Identity(
        nom=request_form['nom'],
        prenom=request_form['pre'],
        spe=request_form['spe1'],
        pot=request_form['pot'],
        pvm=request_form['pvm'],
        nv22=request_form['nv22'],
        cib=request_form['cib'],
    )
    db.session.add(new_pds)
    db.session.commit()

    response = Identity.query.get(id).toDict()
    return jsonify(response)


def retrieve_pds_ctrlr(pds_id):
    con = Connections.query.filter(Connections.doc_id == pds_id).first()
    doc = con.doc
    cdb = con.cdb

    if cdb.ddv is not None and isinstance(cdb.ddv, datetime):
        cdb.ddv = pd.to_datetime(cdb.ddv)
    if cdb.dpv is not None and isinstance(cdb.dpv, datetime):
        cdb.dpv = pd.to_datetime(cdb.dpv)

    return doc, cdb


def delete_pds_ctrlr(pds_id):
    Identity.query.filter_by(id=pds_id).delete()
    db.session.commit()

    return ('Identity with Id "{}" deleted successfully!').format(pds_id)


def update_pds_ctrlr(pds_id, form, url):

    con = Connections.query.filter(Connections.doc_id == pds_id).first()
    identity = con.doc
    adress = con.adr
    cdb = con.cdb

    reques_form = request.form.to_dict()

    ddv = None
    dpv = None

    if not pd.isnull(form["ddv"]) and form["ddv"] != '':
         ddv = datetime.utcfromtimestamp(pd.to_datetime(form["ddv"], dayfirst=False).timestamp())
    if not pd.isnull(form["rdv"]) and form["rdv"] != '':
        dpv = cdb.dpv = datetime.utcfromtimestamp(pd.to_datetime(form["rdv"], dayfirst=True).timestamp())

    cdb.mode = form['mode']
    cdb.com = form['com']
    cdb.ddv = ddv
    cdb.dpv = dpv
    #cdb.rdv = form["rdv"]
    cdb.rec = form["rec"]
    cdb.pk = form["pk"]
    cdb.lun_mat = form.get('lun_mat')
    cdb.lun_am = form.get('lun_am')
    cdb.mar_mat = form.get('mar_mat')
    cdb.mar_am = form.get('mar_am')
    cdb.mer_mat = form.get('mer_mat')
    cdb.mer_am = form.get('mer_am')
    cdb.jeu_mat = form.get('jeu_mat')
    cdb.jeu_am = form.get('jeu_am')
    cdb.ven_mat = form.get('ven_mat')
    cdb.ven_am = form.get('ven_am')

    adress.adr = form.get('adr')
    adress.cp = form.get('cp')
    adress.ville = form.get('ville')

    db.session.commit()

    flash("UPDATE SUCCESSFUL ??", category="warning")

    return redirect(url)



def update_pharma_ctrlr(pha_id, form, url):

    pharma = Pharmacy.query.filter(Pharmacy.id==pha_id).first()
    ddv = None
    rdv = None

    if not pd.isnull(form["ddv"]) and form["ddv"] != '':
        ddv = datetime.utcfromtimestamp(pd.to_datetime(form["ddv"], dayfirst=True).timestamp())
    if not pd.isnull(form["rdv"]) and form["rdv"] != '':
        rdv = datetime.utcfromtimestamp(pd.to_datetime(form["rdv"], dayfirst=True).timestamp())

    pharma.com = form.get('com')
    pharma.ddv = ddv
    pharma.rdv = rdv

    db.session.commit()

    flash("UPDATE SUCCESSFUL", category="success")

    return redirect(url)