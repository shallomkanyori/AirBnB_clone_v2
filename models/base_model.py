#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from datetime import datetime


class BaseModel:
    """A base class for all hbnb models"""

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""

        if not kwargs or 'created_at' not in kwargs.keys():
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)

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
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates updated_at with current time when instance is changed"""

        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""

        dictionary = {}
        dictionary.update(self.__dict__)

        dictionary['__class__'] = type(self).__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        return dictionary
