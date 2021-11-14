# -*- coding: utf-8 -*-
"""Learning Object models."""
from app.database import Column, PkModel, db


class LearningObjects(PkModel):

    __tablename__ = "learning_objects"
    lo_id = Column(db.Text, unique=True, primary_key=True, nullable=False)
    lo_title = Column(db.Text, unique=True, nullable=True)
    supplier = Column(db.Text, unique=True, nullable=True)
    lo_description = Column(db.Text, unique=True, nullable=True)
    lo_type = Column(db.Text, unique=True, nullable=True)
    active_status = Column(db.Boolean, unique=True, nullable=True)
    parent_subject = Column(db.Text, unique=True, nullable=True)
    subject = Column(db.Text, unique=True, nullable=True)
    original_supplier = Column(db.Text, unique=True, nullable=True)
    original_lo_title = Column(db.Text, unique=True, nullable=True)
    original_lo_description = Column(db.Text, unique=True, nullable=True)
    matching_jobs = Column(db.Text, unique=True, nullable=True)
    matching_skills = Column(db.Text, unique=True, nullable=True)
    detected_lang = Column(db.String(2), unique=True, nullable=True)
    lo_description_before = Column(db.Text, unique=True, nullable=True)
    lo_title_before = Column(db.Text, unique=True, nullable=True)
    supplier_before = Column(db.Text, unique=True, nullable=True)
    lo_description_no_sw = Column(db.Text, unique=True, nullable=True)
    lo_title_no_sw = Column(db.Text, unique=True, nullable=True)
    supplier_no_sw = Column(db.Text, unique=True, nullable=True)
    word_count = Column(db.Integer, unique=True, nullable=True)
    lemma_lo_description = Column(db.Text, unique=True, nullable=True)
    lemma_lo_title = Column(db.Text, unique=True, nullable=True)
    tfidf_keywords = Column(db.Text, unique=True, nullable=True)
    tfidf_supplier_keywords = Column(db.Text, unique=True, nullable=True)
    score = Column(db.Float, unique=True, nullable=True)
    score_perc = Column(db.Float, unique=True, nullable=True)
    score_supplier = Column(db.Float, unique=True, nullable=True)
    score_supplier_perc = Column(db.Float, unique=True, nullable=True)

    def __init__(self, lo_id, **kwargs):
        """Create instance."""
        super().__init__(name=lo_id, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Learning Object({self.lo_id})>"
