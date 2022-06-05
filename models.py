from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from typing import Union

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    addresses = relationship("AddressBook", back_populates="owner")


# class Location(Base):
#     __tablename__ = 'locations'
#     id = Column(String, primary_key=True, index=True)

#     latitude = Column(String)
#     longitude = Column(String)
#     location = relationship("AddressBook", back_populates="location")

#     # def __str__(self):
#     #     return '[{}, {}]'.format(self.latitude, self.longitude)


class AddressBook(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address_line_1 = Column(String, index=True)
    address_line_2 = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    country = Column(String, index=True)
    latitude = Column(String, index=True)
    longitude = Column(String, index=True)
    # location = Column(String)
    # location_id = Column(Integer, ForeignKey("locations.id"))
    # location = relationship("Location", back_populates="location")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="addresses")
