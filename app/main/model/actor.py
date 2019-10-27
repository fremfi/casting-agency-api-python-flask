from .. import db
from sqlalchemy import Column, String, Integer, DateTime, Enum
from app.main.exceptions import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import enum


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2


class Actor(db.Model):
    __tablename__ = 'actors'

    _id = Column("id", Integer, primary_key=True)
    _name = Column("name", String(120), nullable=False)
    _age = Column("age", Integer, nullable=False)
    _gender = Column("gender", Enum(Gender), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not name:
            raise ValidationError('name cannot be empty.')
        self._name = name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        if not age:
            raise ValidationError("age cannot be empty")
        self._age = age

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        if not gender:
            raise ValidationError("gender cannot be empty")
        if gender not in Gender.__members__:
            raise ValidationError("gender is either MALE or FEMALE")
        self._gender = gender

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def format(self):
        return {
          'id': self._id,
          'name': self._name,
          'age': self._age,
          'gender': self._gender
        }
