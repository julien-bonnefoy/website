from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, DateTimeField, FloatField
from wtforms.validators import InputRequired, Length


class IdentityForm(FlaskForm):
    nom = StringField('nom')
    pre = StringField('prenom')
    spe = StringField('spe1')
    pot = IntegerField("pot")
    pvm = IntegerField("pvm")
    nv22 = IntegerField("nv2022")
    cib = IntegerField("ciblage")
    dec = StringField('dec')
    submit = SubmitField("Submit")


class AdressForm(FlaskForm):
    uga = StringField('uga')
    eta = StringField('eta')
    adr = StringField('adr')
    cp = StringField('cp')
    ville = StringField('vil')
    tel = StringField('tel')
    lat = FloatField('lat')
    lon = FloatField('lon')
    submit = SubmitField("Submit")


class CdbForm(FlaskForm):
    mode = StringField('mode')
    com = TextAreaField('com')
    ddv = DateTimeField("ddv", format="%d/%m/%Y %H:%M")
    dpv = DateTimeField("rdv", format="%d/%m/%Y %H:%M")
    rdv = StringField("rdv")
    rec = StringField("rec")
    pk = StringField("pk")
    lun_mat = StringField('lun_mat')
    lun_am = StringField('lun_am')
    mar_mat = StringField('mar_mat')
    mar_am = StringField('mar_am')
    mer_mat = StringField('mer_mat')
    mer_am = StringField('mer_am')
    jeu_mat = StringField('jeu_mat')
    jeu_am = StringField('jeu_am')
    ven_mat = StringField('ven_mat')
    ven_am = StringField('ven_am')
    submit = SubmitField("Submit")


class ConnectionForm(FlaskForm):
    doc_id = IntegerField("Doc Id")
    adr_id = IntegerField("Adr Id")
    cdb_id = IntegerField("Cdb Id")
    submit = SubmitField("Update")


class MegaForm(FlaskForm):
    id = IntegerField('id')
    nom = StringField('nom')
    pre = StringField('prenom')
    spe = StringField('spe1')
    pot = IntegerField("pot")
    pvm = IntegerField("pvm")
    nv22 = IntegerField("nv2022")
    cib = IntegerField("ciblage")
    dec = StringField('dec')
    uga = StringField('uga')
    eta = StringField('eta')
    adr = StringField('adr')
    cp = StringField('cp')
    ville = StringField('vil')
    tel = StringField('tel')
    lat = FloatField('lat')
    lon = FloatField('lon')
    mode = StringField('mode')
    com = TextAreaField('com')
    ddv = DateTimeField("ddv", format="%d/%m/%Y %H:%M")
    dpv = DateTimeField("rdv", format="%d/%m/%Y %H:%M")
    rdv = StringField("rdv")
    rec = StringField("rec")
    pk = StringField("pk")
    lun_mat = StringField('lun_mat')
    lun_am = StringField('lun_am')
    mar_mat = StringField('mar_mat')
    mar_am = StringField('mar_am')
    mer_mat = StringField('mer_mat')
    mer_am = StringField('mer_am')
    jeu_mat = StringField('jeu_mat')
    jeu_am = StringField('jeu_am')
    ven_mat = StringField('ven_mat')
    ven_am = StringField('ven_am')
    submit = SubmitField("Submit")