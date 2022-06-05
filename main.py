from turtle import distance
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/addresses/", response_model=schemas.AddressBook)
def create_address_for_user(
    user_id: int, address: schemas.AddressBookCreate, db: Session = Depends(get_db)
):
    return crud.create_user_address(db=db, address=address, user_id=user_id)


@app.get("/addresses/", response_model=list[schemas.AddressBook])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db, skip=skip, limit=limit)
    return addresses


@app.post("/distance/")
def calculate_distance(city: str, city1: str, db: Session = Depends(get_db)):
    distance = crud.get_nearby_locations(db, city, city1)
    return distance


@app.post("/nearby_addresses/")
def find_nearby_addresses(address_id: int, distance_in_km: int, db: Session = Depends(get_db)):
    nearby_addresses = crud.get_nearby_addresses(
        address_id, distance_in_km, db)

    return nearby_addresses
