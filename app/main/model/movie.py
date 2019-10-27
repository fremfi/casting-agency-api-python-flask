from .. import db
from sqlalchemy import Column, String, Integer, DateTime
from app.main.exceptions import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class Movie(db.Model):
    __tablename__ = 'movies'

    _id = Column("id", Integer, primary_key=True)
    _title = Column("title", String(120), nullable=False)
    _release_date = Column("release_date", DateTime(), nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if not title:
            raise ValidationError('title cannot be empty.')
        self._title = title

    @property
    def release_date(self):
        return self._release_date

    @release_date.setter
    def release_date(self, release_date):
        if not release_date:
            raise ValidationError("release date cannot be empty")
        try:
            datetime.strptime(release_date, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('release_date format should be YYYY-MM-DD')

        self._release_date = release_date

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
          'title': self._title,
          'release_date': self._release_date
        }
