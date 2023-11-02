from flask import request, jsonify, flash, redirect, url_for
from application.pds.models import db, Cdb, Connections, Identity, Adress
import pandas as pd
import numpy as np
from sqlalchemy import func, TIMESTAMP
from datetime import datetime

# ----------------------------------------------- #

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
        prenom=request_form['prenom'],
        spe=request_form['spe'],
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


def update_pds_ctrlr(pds_id):
    form = request.form.to_dict()
    con = Connections.query.filter(Connections.doc_id == pds_id).first()
    doc = con.doc
    cdb = con.cdb
    ddv = None
    dpv = None

    if  form["ddv"] and form["ddv"] != '':
         ddv = datetime.utcfromtimestamp(pd.to_datetime(form["ddv"], dayfirst=True).timestamp())
    if  form["dpv"] and form["dpv"] != '':
        dpv = cdb.dpv = datetime.utcfromtimestamp(pd.to_datetime(form["dpv"], dayfirst=True).timestamp())

    cdb.mode = form['mode']
    cdb.com = form['com']
    cdb.ddv = ddv
    cdb.dpv = dpv
    cdb.rdv = form["rdv"]
    cdb.rec = form["rec"]
    cdb.pk = form["pk"]
    cdb.lun_mat = form['lun_mat']
    cdb.lun_am = form['lun_am']
    cdb.mar_mat = form['mar_mat']
    cdb.mar_am = form['mar_am']
    cdb.mer_mat = form['mer_mat']
    cdb.mer_am = form['mer_am']
    cdb.jeu_mat = form['jeu_mat']
    cdb.jeu_am = form['jeu_am']
    cdb.ven_mat = form['ven_mat']
    cdb.ven_am = form['ven_am']

    db.session.commit()

    flash("UPDATE SUCCESSFUL ??", category="warning")

    return redirect(url_for("home_bp.home"))
