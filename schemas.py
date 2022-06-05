from pydantic import BaseModel


# class LocationBase(BaseModel):
#     latitude: str | None = None
#     longitude: str | None = None


# class LocationCreate(LocationBase):
#     pass


# class Location(LocationBase):
#     id = int


class AddressBookBase(BaseModel):
    name: str
    address_line_1: str
    address_line_2: str | None = None
    city: str
    country: str
    latitude: str | None = None
    longitude: str | None = None


class AddressBookCreate(AddressBookBase):
    pass


class AddressBook(AddressBookBase):
    id: int
    location_id = int
    owner_id = int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    addresses: list[AddressBook] = []

    class Config:
        orm_mode = True
