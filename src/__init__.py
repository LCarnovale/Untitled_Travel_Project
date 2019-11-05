import sys
sys.path.append('src/')

import db
if not db.is_connected:
    db.init()

import accommodation
import accommodationSystem
import address
import bookingSystem
import booking
import search
import user
import userSystem