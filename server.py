from flask import Flask
from init import bootstrap_system
from accommodation_system import AccommodationSystem

app = Flask(__name__)
app.secret_key = 'very-secret-123'  # Used to add entropy
system = AccommodationSystem()
bootstrap_system()