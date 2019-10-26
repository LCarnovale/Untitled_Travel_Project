from flask import Flask
from init import bootstrap_system
from src.accommodationSystem import AccommodationSystem
from src.userSystem import UserSystem
from src.bookingSystem import BookingSystem


app = Flask(__name__)
app.secret_key = 'very-secret-123'  # Used to add entropy TODO: Learn what this is actually for
accSystem = AccommodationSystem()
userSystem = UserSystem()
bookingSystem = BookingSystem()
bootstrap_system()

