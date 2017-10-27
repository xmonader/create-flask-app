from enum import Enum
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listen
import string
import random


db = SQLAlchemy()
db.session.autocommit = True


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean(), default=False)
    # timestamps
    created_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

