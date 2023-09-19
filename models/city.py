#!/usr/bin/python3
""" City Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.place import Place


class City(BaseModel, Base):
    """Represents a City.

    Attributes:
        state_id: the id of the city's state.
        name: the name of the city.
    """

    __tablename__ = 'cities'

    if models.storage_type == 'db':
        state_id = Column(String(128), ForeignKey('states.id'), nullable=False)
        name = Column(String(60), nullable=False)

    else:
        state_id = ""
        name = ""

    places = relationship("Place", cascade="all, delete", backref="cities")
