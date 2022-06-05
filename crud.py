from sqlalchemy import not_
from sqlalchemy.orm import Session
from sqlalchemy.sql import not_, select


import models
import schemas

from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def get_location(city_name):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(city_name)

    def get_coordinates(city_name):

        return getLoc.latitude, getLoc.longitude
    return getLoc


def get_coordinates(city_name):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(city_name)
    return getLoc.latitude, getLoc.longitude


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AddressBook).offset(skip).limit(limit).all()


def create_user_address(db: Session, address: schemas.AddressBookCreate, user_id: int):
    location = get_location(address.city)
    address.latitude = str(location.latitude)
    address.longitude = str(location.longitude)
    db_address = models.AddressBook(**address.dict(), owner_id=user_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def calculate_distance(city1: str, city2: str):
    """Accepts city names and returns the distance between the cities based on the location coordinates"""
    city1 = get_coordinates(city1)
    city2 = get_coordinates(city2)
    distance = geodesic(city1, city2).km
    return distance


def get_nearby_addresses(address_id: int, distance_in_km: int, db: Session):
    """Accepts an address id, and distance in Kilometers. Returns a list of addresses found within this distance"""
    user_input_address = db.query(models.AddressBook).filter(
        models.AddressBook.id == address_id).first()
    user_input_city = user_input_address.city
    all_addresses = db.query(models.AddressBook).all()
    selected_addresses = []
    for address in all_addresses:
        if address_id != address.id:
            calculated_distance = calculate_distance(
                user_input_city, address.city)
            if calculated_distance < distance_in_km:
                selected_addresses.append(address)
    return selected_addresses
