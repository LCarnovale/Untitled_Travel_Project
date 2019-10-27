from flask import Flask
from init import bootstrap_system
from src.accommodationSystem import AccommodationSystem
from src.userSystem import UserSystem

from src.address import Address
from src.user import User
from src.stayDetails import StayDetails
from src.accommodation import Accommodation

USE_DATABASE = False

app = Flask(__name__)
app.secret_key = 'very-secret-123'  # Used to add entropy
accSystem = AccommodationSystem()
userSystem = UserSystem()
bootstrap_system()


# DUMMY PEOPLE


# Make an owner class
owner = User('Jim', 'example@gmail.com', '0400 000 000', 'Owner detials')
# Make an address class
addr = Address('Addr')

# Make a stay class
stay = StayDetails('500', '10-10-2020, 10-10-2021', '100', '200', 'No pets')
# Make an accommodation class
acc = Accommodation('HELLO wold__D_ epic', addr, '5', '5', owner, stay, 'Pet pets wow pets beds wow big score')
# Add the accommodation into the system
accSystem.addAcc(acc)
print(acc.getID())
# Add the user into the system
userSystem.addUser(owner)

acc = Accommodation('HELLO', addr, '5', '5', owner, stay, 'No pets are allowed in this house please')
# Add the accommodation into the system
accSystem.addAcc(acc)

print(acc.getID())
