Hotel Management System

A backend for managing a hotel's rooms, guests and bookings, built with FastAPI and PostgreSQL. This is a learning project; the frontend is planned next.

Features (so far)

Rooms, guests and bookings endpoints (create, read, update, delete)
Booking logic tested through the interactive Swagger docs (/docs)
Guest registration and authentication with a secret key loaded from .env
Request/response validation with Pydantic schemas
PostgreSQL database access through SQLAlchemy and the psycopg (v3) driver

Tech Stack

Python, FastAPI, Uvicorn
PostgreSQL, SQLAlchemy, psycopg
Pydantic, python-dotenv
