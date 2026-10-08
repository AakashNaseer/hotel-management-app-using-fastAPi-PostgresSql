from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date


# this portion is for ROOM ---
class RoomCreate(BaseModel):
    room_number: str
    room_type: str
    price_per_night: float


class RoomResponse(RoomCreate):
    id: int
    is_available: bool

    model_config = ConfigDict(from_attributes=True)


# this portion is for GUEST ----
class GuestCreate(BaseModel):
    name: str
    phone: str
    email: str | None = None
    cnic: str | None = None


class GuestResponse(GuestCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


# this portion is for BOOKING -----
class BookingCreate(BaseModel):
    guest_id: int
    room_id: int
    check_in: date
    check_out: date


class BookingResponse(BaseModel):
    id: int
    guest_id: int
    room_id: int
    check_in: date
    check_out: date
    total_price: float
    status: str

    model_config = ConfigDict(from_attributes=True)

# this portion is for user_auth etc

class GuestRegister(BaseModel):
    full_name: str
    email: str
    password: str


class AdminRegister(GuestRegister):
    admin_secret:str


class UserOut(BaseModel):
    id : int
    full_name:str
    email: EmailStr
    role: str
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type : str

