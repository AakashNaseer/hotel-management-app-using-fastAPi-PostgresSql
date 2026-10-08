from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ------- ROOMS

@app.post("/rooms", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Room).filter(
        models.Room.room_number == room.room_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Room number already exists")

    new_room = models.Room(**room.model_dump())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@app.get("/rooms", response_model=list[schemas.RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).all()


@app.get("/rooms/{room_id}", response_model=schemas.RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@app.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room)
    db.commit()
    return {"message": "Room deleted"}


# ------- GUESTS

@app.post("/guests", response_model=schemas.GuestResponse)
def create_guest(guest: schemas.GuestCreate, db: Session = Depends(get_db)):
    new_guest = models.Guest(**guest.model_dump())
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)
    return new_guest


@app.get("/guests", response_model=list[schemas.GuestResponse])
def get_guests(db: Session = Depends(get_db)):
    return db.query(models.Guest).all()


@app.get("/guests/{guest_id}", response_model=schemas.GuestResponse)
def get_guest(guest_id: int, db: Session = Depends(get_db)):
    guest = db.query(models.Guest).filter(models.Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest


@app.delete("/guests/{guest_id}")
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    guest = db.query(models.Guest).filter(models.Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    db.delete(guest)
    db.commit()
    return {"message": "Guest deleted"}


# ------- BOOKINGS

@app.post("/bookings", response_model=schemas.BookingResponse)
def create_booking(data: schemas.BookingCreate, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == data.room_id).first()
    guest = db.query(models.Guest).filter(models.Guest.id == data.guest_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    if data.check_out <= data.check_in:
        raise HTTPException(status_code=400, detail="Check-out must be after check-in")

    clash = db.query(models.Booking).filter(
        models.Booking.room_id == data.room_id,
        models.Booking.status == "booked",
        models.Booking.check_in < data.check_out,
        models.Booking.check_out > data.check_in,
    ).first()
    if clash:
        raise HTTPException(status_code=409, detail="Room already booked for these dates")

    nights = (data.check_out - data.check_in).days
    total = nights * room.price_per_night

    booking = models.Booking(
        guest_id=data.guest_id,
        room_id=data.room_id,
        check_in=data.check_in,
        check_out=data.check_out,
        total_price=total,
        status="booked",
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@app.get("/bookings", response_model=list[schemas.BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).all()


@app.put("/bookings/{booking_id}/checkout")
def checkout(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = "completed"
    db.commit()
    return {"message": "Checked out successfully"}