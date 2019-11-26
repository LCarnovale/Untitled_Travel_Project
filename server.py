from flask import Flask
from src.accommodationSystem import AccommodationSystem
from src.userSystem import UserSystem
from src.bookingSystem import BookingSystem

from src.address import Address
from src.user import User
from src.accommodation import Accommodation

USE_DATABASE = True
RESULTS_PER_PAGE = 21 # 7 rows of 3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'bottom-secret'
accSystem = AccommodationSystem()
userSystem = UserSystem()
bookingSystem = BookingSystem()