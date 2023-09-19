#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Represents an amenity."""

    __tablename__ = 'amenities'

    if models.storage_type == 'db':
        name = Column(String(128), nullable=False)

        place_amenities = relationship('Place', secondary='place_amenity',
                                       back_populates='amenities',
                                       viewonly=False)
    else:
        name = ""
