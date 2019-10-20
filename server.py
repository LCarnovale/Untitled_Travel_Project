from flask import Flask
from init import bootstrap_system
from src.accommodationSystem import AccommodationSystem
from src.userSystem import UserSystem

DBG_current_commit = ""

app = Flask(__name__)
app.secret_key = 'very-secret-123'  # Used to add entropy
accSystem = AccommodationSystem()
userSystem = UserSystem()
bootstrap_system()
