#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.review import Review

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

places_amenities = Table('place_amenity', Base.metadata,
                         Column('place_id', String(60),
                                ForeignKey('places.id'),
                                primary_key=True),
                         Column('amenity_id', String(60),
                                ForeignKey('amenities.id'),
                                primary_key=True)
                         )


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = 'places'

    if models.storage_type == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        reviews = relationship('Review', cascade='all, delete, delete-orphan',
                               backref='place')

        amenities = relationship('Amenity', secondary='place_amenity',
                                 back_populates='place_amenities',
                                 viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Returns all reviews associated with the current instance."""

            reviews_res = models.storage.all(Review).values()

            res = [r for r in reviews_res if r.place_id == self.id]

            return res

        @property
        def amenities(self):
            """Returns all amenities linked to the current instance."""

            amenities_res = models.storage.all(Amenity).values()

            res = [a for a in amenities_res if a.id in self.amenity_ids]

            return res

        @amenities.setter
        def amenities(self, val):
            if type(val) is Amenity:
                self.amenity_ids.append(val.id)
