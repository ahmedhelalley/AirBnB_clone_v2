#!/usr/bin/python3
""" Place Module for HBNB project """
import os

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base

place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True),
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column('city_id', String(60), ForeignKey('cities.id'),
                     nullable=False)
    user_id = Column('user_id', String(60), ForeignKey('users.id'),
                     nullable=False)
    name = Column('name', String(128), nullable=False)
    description = Column('description', String(1024))
    number_rooms = Column('number_rooms', Integer, default=0, nullable=False)
    number_bathrooms = Column('number_bathrooms', Integer, default=0,
                              nullable=False)
    max_guest = Column('max_guest', Integer, default=0, nullable=False)
    price_by_night = Column('price_by_night', Integer, default=0,
                            nullable=False)
    latitude = Column('latitude', Float)
    longitude = Column('longitude', Float)
    amenity_ids = []
    reviews = relationship('Review', backref='place', cascade='all, delete')
    amenities = relationship('Amenity', secondary='place_amenity',
                             viewonly=False)

    if os.getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Get/set linked Reviews"""
            return [review for review in self.reviews if
                    review.place_id == self.id]

        @property
        def amenities(self):
            """Get/set linked Amenities"""
            amenity_list = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, amenity):
            """Get/set linked Amenities"""
            if type(amenity) == Amenity:
                self.amenity_ids.append(amenity.id)
