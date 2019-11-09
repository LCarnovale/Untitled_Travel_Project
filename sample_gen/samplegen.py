"""
Create sample data for the database.

Creation process:

1) Create owners
2) Create addresses
3) Create venues attached to random existing owners and addresses,
   with randomly generated availabilities.
4) Create users
5) Create bookings attached to random existing users and venues
6) Create reviews for random existing venues and users, for users
   that have made a booking at the given venue.
"""

import sys
sys.path.append("../")
sys.path.append("../src/")
sys.path.append("../db/")
import datetime
import src
import db
import random

def _load_text(filename):
    with open(filename, 'r') as f:
        lines = f.read().split('\n')
        return [l for l in lines if l] # remove empty lines

adjectives = _load_text('adjectives.txt')
nouns = _load_text('nouns.txt')
adverbs = _load_text('adverbs.txt')
types = _load_text('types.txt')
fullnames = _load_text('fullnames.txt')
firstnames = [f.split(' ')[0] for f in fullnames]
lastnames  = [f.split(' ')[1] for f in fullnames]
passwords = ['1234', '12345', 'password', 'password1', 'hello']
# Boundary for generated locations
map_poly = [ # Rouhgly surrounds NSW
    (-29.052491, 141.192756),
    (-28.958767, 153.359836),
    (-37.035049, 148.950993),
    (-33.889928, 141.232345)
]

# Will be filled as more are generated to keep track of foreign keys etc.
_owner_ids = [7, 8, 9, 10, 11]
_user_ids = []
_address_ids = [33, 34, 35, 36, 37]
_venue_ids = [21, 22]
_booking_ids = []
_avail_ids = [20, 21, 22, 23, 24, 25]


def is_in_polygon(point, polygon, latlng=True):
    """Check if the given point is inside the polygon.
    point should be an (lat, lon) pair, polygon should be a list
    of (lat, lon) pairs, ordered clockwise
    
    This probably only works on basic polygons, ie where all vertices
    have internal angles less than 180 degrees.
    
    To use xy coordinates set `latlng=False`."""

    if latlng:
        point = (point[1], point[0])
        polygon = [(y, x) for (x, y) in polygon]

    n = len(polygon)
    x, y = point

    last = polygon[-1]

    inside = True
    for p in polygon:
        # check if the point lies to the right
        # of the line from last to p
        px, py = p
        lx, ly = last
        # gradient:
        m = (py - ly) / (px - lx)
        # If this is positive then the point is on the right side of the line
        s = m*x - y - m*lx + ly
        s *= (px - lx)
        inside &= s > 0
        last = p
    return inside

def random_venue_names(n=1):
    """
    Create `n` (default 1) name(s) that look like:
    ' The {adverb} {adjective} {noun} {venue type} '
    venue type will be one of inn, holiday park, hotel etc.
    """
    # max_n = max(len(adjectives), len(nouns), len(adverbs), len(types))
    # n = min(max_n, n)
    if n < 0:
        raise ValueError("n must be greater than zero.")

    adverb_sample    =  [x.capitalize() for x in random.choices(adverbs, k=n)]
    noun_sample      =  [x.capitalize() for x in random.choices(nouns, k=n)]
    adjective_sample =  [x.capitalize() for x in random.choices(adjectives, k=n)]
    type_sample      =  [x.capitalize() for x in random.choices(types, k=n)]

    names = [
        f"The {adverb_sample[i]} {adjective_sample[i]} {noun_sample[i]} {type_sample[i]}"
        for i in range(n)
    ]

    return names

def random_fullnames(n=1):
    """
    Create `n` (default 1) full names (firstname lastname).
    Returns a list of names.
    """
    firstname_choices = random.choices(firstnames, k=n)
    lastname_choices = random.choices(lastnames, k=n)
    fullnames = [f"{firstname_choices[i]} {lastname_choices[i]}" for i in range(n)]

    return fullnames

def random_usernames(n=1):
    """
    Create `n` (default 1) random usernames.
    The usernames will look like {random noun}xxx
    where xxx is 3 random digits.
    """
    noun_samples = random.choices(nouns, k=n)
    digit_samples = [
        f"{random.randint(0,999):03d}" for _ in range(n)
    ]
    usernames = [
        f"{noun_samples[i]}{digit_samples[i]}" for i in range(n)
    ]
    return usernames

def random_passwords(n=1):
    return random.choices(passwords, k=n)

def random_emails(n=1):
    """Generate n random email addresses with the form:
    {random username}@{random domain}.com"""
    domains = ['gmail', 'hotmail', 'yahoo', 'outlook']
    domain_choices = random.choices(domains, k=n)
    name_choices = random_usernames(n)

    emails = [
        f"{name_choices[i]}@{domain_choices[i]}.com" for i in range(n)
    ]

    return emails

def random_phones(n=1):
    """Returns a list of n random 8 digit phone numbers."""
    nums = [
        f"{random.randint(10000000, 99999999):08d}" for i in range(n)
    ]
    return nums

def random_locations(n=1, boundary=map_poly):
    """Create n random locations within the given polygon,
    by default roughly the boundary around NSW.
    
    If providing a boundary, it must be a list of (lat, lon) pairs."""
    
    lats = [x for (x, y) in boundary]
    lons = [y for (x, y) in boundary]
    min_lat = min(lats)
    max_lat = max(lats)
    min_lon = min(lons)
    max_lon = max(lons)

    lat_choices = [
        random.random() * (max_lat - min_lat) + min_lat for i in range(3*n)
    ]
    lon_choices = [
        random.random() * (max_lon - min_lon) + min_lon for i in range(3*n)
    ]
    coords = [
        (lat, lon) for (lat, lon) in zip(lat_choices, lon_choices) \
        if is_in_polygon((lat, lon), boundary)
    ]
    return coords[:n]

def create_owners(n=1):
    """Create n owners with a random name, username, password, email and phone
    and insert them into the database.
    
    Returns a list of ids of the created owners."""

    fullnames = random_fullnames(n)
    usernames = random_usernames(n)
    emails = random_emails(n)
    phones = random_phones(n)
    passwords = random_passwords(n)
    
    description = "Randomly generated description"

    generated = []

    for i in range(n):
        try:
            ownerid = db.owners.insert(fullnames[i], usernames[i], passwords[i],
                            emails[i], phones[i], description + f" (my password is {passwords[i]})")
        except db.InsertionError as e:
            print("Error occured while inserting user with data:")
            print(f"Name: {fullnames[i]} Username: {usernames[i]} Password: {passwords[i]}")
            print(f"Emails: {emails[i]} Phone: {phones[i]} Description: {description}")
            print("Error:")
            print(e)
        else:
            _owner_ids.append(ownerid)
            generated.append(ownerid)

    return generated

def create_addresses(n=1):
    """ Create n random addresses and store them in the database,
    with the label 'Randomly generated street address'."""
    locations = []
    while len(locations) < n:
        locations = random_locations(n)
    
    generated = []

    for i in range(n):
        loc = locations[i]
        aid = db.addresses.insert(
            "Randomly generated street address.", 
            f"{loc[0]:.6f}", f"{loc[1]:.6f}"
        )
        _address_ids.append(aid)
        generated.append(aid)

    return generated

def create_venues(n=1):
    """Create n random addresses, then n random venues and store them in the database.
    Also creates availabilities for each venue."""
    if not _address_ids:
        raise Exception("Address IDs empty. Need to make some before making venues.")
    if not _owner_ids:
        raise Exception("Owner IDs empty. Need to make some before making venues.")

    

    owners = random.choices(_owner_ids, k=n)
    addresses = create_addresses(n) #random.choices(_address_ids, k=n)
    names = random_venue_names(n)
    beds = [random.randint(1, 10) for i in range(n)]
    baths = [random.randint(1, 10) for i in range(n)]
    cars = [random.randint(1, 10) for i in range(n)]
    description = "Randomly generated venue description"
    rates = [random.random()*250 for i in range(n)]
    minStays = [random.randint(1, 3) for i in range(n)]
    maxStays = [random.randint(5, 50) for i in range(n)]
    details = "Randomly generated venue details"

    ranges = [random.randint(1, 4) for i in range(n)]
    for i in range(n):
        venueid = db.venues.insert(
            owners[i], addresses[i], names[i], beds[i],
            baths[i], cars[i], description, rates[i], minStays[i], 
            maxStays[i], details
        )    
        _venue_ids.append(venueid)

        # Create availabilities
        lastDate = datetime.date.today()
        for r in range(ranges[i]):
            lastDate += datetime.timedelta(days=random.randint(3, 10))
            dt = datetime.timedelta(days=random.randint(10, 200))
            avid = db.availabilities.insert(venueid, lastDate, lastDate + dt)
            lastDate += dt
            _avail_ids.append(avid)

# def create_availabilities(n=1):
#     if not _venue_ids:
#         raise Exception("Venue IDs empty. Need to make some before making availabilities.")
#     ranges = [random.randint(1, 4) for i in range(n)]
#     venues = random.choices(_venue_ids, k=n)
#     for i in range(n):
#         lastDate = datetime.date.today()
#         for r in range(ranges[i]):
#             lastDate += datetime.timedelta(days=random.randint(3, 10))
#             dt = datetime.timedelta(days=random.randint(10, 200))
#             avid = db.availabilities.insert(venues[i], lastDate, lastDate + dt)
#             lastDate += dt
#             _avail_ids.append(avid)

            
    


def clean():
    """Remove all database entries created by this program."""
    pass
