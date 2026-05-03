#!/usr/bin/env python3
"""Run once after first docker-compose up to create the admin user."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models import User
from app.utils.security import hash_password

USERNAME = os.getenv("ADMIN_USERNAME", "admin")
EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme123")

db = SessionLocal()
try:
    existing = db.query(User).filter(User.username == USERNAME).first()
    if existing:
        print(f"Admin user '{USERNAME}' already exists.")
    else:
        user = User(
            username=USERNAME,
            email=EMAIL,
            hashed_password=hash_password(PASSWORD),
            is_admin=True,
        )
        db.add(user)
        db.commit()
        print(f"Admin user '{USERNAME}' created successfully.")
finally:
    db.close()
