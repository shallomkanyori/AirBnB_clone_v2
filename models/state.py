#!/usr/bin/python3
""" State Module for HBNB project """
import os
import models
from models.base_model import BaseModel, Base
from models.city import City

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Represent a State.

    Attributes:
        name: the name of the state.
    """

    __tablename__ = 'states'

    if models.storage_type == 'db':
        name = Column(String(128), nullable=False)

        cities = relationship('City', backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            cities_res = models.storage.all(City).values()

            res = [c for c in cities_res if c.state_id == self.id]

            return res
