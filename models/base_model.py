#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(),
                        nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(),
                        nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""

        if not kwargs or 'created_at' not in kwargs.keys():
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

        if kwargs:
            keys = kwargs.keys()

            for attr in keys:
                if attr == "__class__":
                    continue

                elif attr == "created_at" or attr == "updated_at":
                    kwargs[attr] = datetime.strptime(kwargs[attr],
                                                     '%Y-%m-%dT%H:%M:%S.%f')

                setattr(self, attr, kwargs[attr])

            if 'created_at' in keys:
                if 'id' not in keys:
                    setattr(self, 'id', str(uuid.uuid4()))

                if 'updated_at' not in keys:
                    setattr(self, 'updated_at', datetime.utcnow())

    def __str__(self):
        """Returns a string representation of the instance"""
        res = {}
        res.update(self.__dict__)

        del_key = '_sa_instance_state'
        if del_key in res.keys():
            del res[del_key]

        return f"[{type(self).__name__}] ({self.id}) {res}"

    def save(self):
        """Updates update_at and saves the instance to storage."""

        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""

        res = {}
        res.update(self.__dict__)

        del_key = '_sa_instance_state'
        if del_key in res.keys():
            del res[del_key]

        res['__class__'] = type(self).__name__
        res['created_at'] = self.created_at.isoformat()
        res['updated_at'] = self.updated_at.isoformat()

        return res

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)
