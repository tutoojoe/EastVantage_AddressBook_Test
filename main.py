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
    """Creates a user in database"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Returns a list of all the users in the database"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Returns the user based on the given ID"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/addresses/", response_model=schemas.AddressBook)
def create_address_for_user(
        user_id: int, address: schemas.AddressBookCreate, db: Session = Depends(get_db)):
    """Creates an address for the user. A user can create multiple addresses
    Location and address fields will be autopopulated"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_address(db=db, address=address, user_id=user_id)


@ app.get("/addresses/", response_model=list[schemas.AddressBook])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Returns a list of all the addresses in the database"""
    addresses = crud.get_addresses(db, skip=skip, limit=limit)
    return addresses


@ app.post("/nearby_addresses/")
def find_nearby_addresses(address_id: int, distance_in_km: int, db: Session = Depends(get_db)):
    """Returns a list of all the nearby addresses in the database, within the given distance parameter"""
    db_address = crud.get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(
            status_code=404, detail="The given address id is not found. Pleases re-enter.")
    nearby_addresses = crud.get_nearby_addresses(
        address_id, distance_in_km, db)
    return nearby_addresses
