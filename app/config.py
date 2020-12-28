"""Global configurations for the whole application."""
import os

DATABASE_DNS = os.getenv("DATABASE_DNS")
SECRET_KEY = os.getenv("SECRET_KEY")
