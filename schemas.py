from pydantic import BaseModel


class AddressBookBase(BaseModel):
    name: str
    door_no: str
    street_name: str | None = None
    address: str | None = None
    latitude: str | None = None
    longitude: str | None = None
    city: str


class AddressBookCreate(AddressBookBase):
    pass


class AddressBook(AddressBookBase):
    id: int
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
