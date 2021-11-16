# -*- coding: utf-8 -*-
from sqlalchemy import  Column, Integer, String, Sequence, Text, Table
from sqlalchemy import ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import redis
import rq
import datetime as dt
from flask_app.database import PkModel, reference_col, db
from flask_app.extensions import bcrypt
import base64
from datetime import datetime, timedelta
from hashlib import md5
import json
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
import jwt
from flask_app.extensions import login_manager

Base = declarative_base()

jobs_skills = Table(
    "jobs_skills",
    Base.metadata,
    Column("job_id", Integer, ForeignKey("job.job_id")),
    Column("skill_id", Integer, ForeignKey("skill.skill_id"))
)


class LearningObjects(Base):
    __tablename__ = "learning_objects"
    index = Column(Integer, Sequence('lo_ix_seq'), primary_key=True)
    lo_id = Column(String)
    lo_title = Column(Text)
    lo_description = Column(Text)
    lemma_lo_title = Column(Text)
    lemma_lo_description = Column(Text)
    active_status = Column(Boolean)
    lo_type = Column(Integer, ForeignKey('types.type_ix'))
    supplier = Column(Integer, ForeignKey('suppliers.supplier_ix'))
    parent_subject = Column(Integer, ForeignKey('categories.category_ix'))


class Suppliers(Base):
    __tablename__ = "suppliers"
    supplier_ix = Column(Integer, Sequence('supplier_ix_seq'), primary_key=True)
    supplier_name = Column(String)


class Types(Base):
    __tablename__ = "types"
    type_ix = Column(Integer, Sequence('type_ix_seq'), primary_key=True)
    type_name = Column(String)


class Categories(Base):
    __tablename__ = "categories"
    category_ix = Column(Integer, Sequence('category_ix_seq'), primary_key=True)
    category_name = Column(String)


class Jobs(Base):
    __tablename__: str = "jobs_table"
    job_id = Column(Integer, primary_key=True)
    jon_name = Column(String)

    skills = relationship(
        "Skill", secondary=jobs_skills, back_populates="jobs"
    )
    learning_objects = relationship(
        "LearningObjects", back_populates="jobs"
    )


class Skill(Base):
    __tablename__: str = "skills_table"
    skill_id = Column(String, primary_key=True)
    skill_name = Column(String)

    jobs = relationship(
        "Job", secondary=jobs_skills, back_populates="skills"
    )
    learning_objects = relationship(
        "LearningObject", back_populates="skills"
    )

