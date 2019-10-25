from flask import render_template, request, redirect, abort
from src.accommodation import Accommodation
from src.accommodationSystem import AccommodationSystem
from src.address import Address
from src.user import User
from src.stayDetails import StayDetails
import src.userSystem
from server import accSystem
from server import userSystem
from server import app
import cloud.dbTools as db

default_kwargs = {
    "is_connected": db.is_connected,
}

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', **default_kwargs)

'''
Landing page
'''
@app.route('/', methods=['GET', 'POST'])
def home():
    
    if request.method == 'POST':
        pass

    return render_template('home.html', **default_kwargs)

'''
Login page
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Attempt a Login
        result = db.check_user_pass(request.form['username'], request.form['password'])
        if result is None:
            print("Login failed")
        else:
            print(f"Log in for {result[1]} ({result[2]}) successful.")

    return render_template('login.html')

'''
Signup page
'''
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Create user.
        form = request.form
        uid = src.userSystem.create_user(
            form['account_name'],
            form['account_username'],
            form['account_password'],
            form['account_email'],
            form['account_phone'],
            form['account_description']
        )

        if uid is not None:
            print("User successfully added.")
        else:
            print("User insert failed.")


    return render_template('signup.html')

'''
Main Booking page
'''  
@app.route('/book/<id>', methods=['GET', 'POST'])
def book_main(id):
    acc = accSystem.getAcc(id)
    print(acc)
    if acc == None:
        abort(404)

    if request.method == 'POST':
        pass #TODO

    return render_template('book.html', acc=acc, **default_kwargs)



'''
Main Post accommodation page
'''  
@app.route('/post_ad', methods=['GET', 'POST'])
def ad_main():
    if request.method == "POST":
        # Make an owner class
        owner = User(request.form['own_name'], request.form['own_email'],
                    request.form['own_phone'], request.form['own_details'])
        # Make an address class
        addr = Address(request.form['acc_addr'])

        # Make a stay class
        stay = StayDetails(request.form['price'], request.form['avail_date'],
                        request.form['min_stay'],
                        request.form['max_stay'], request.form['stay_details'])
        # Make an accommodation class
        acc = Accommodation(request.form['acc_name'], addr,
                        request.form['acc_nbed'], request.form['acc_nbath'],owner, stay, request.form['acc_details'],)
        # Add the accommodation into the system
        accSystem.addAcc(acc)
        # Add the user into the system
        userSystem.addUser(owner)
        return render_template('ad_confirm.html', id=acc.getID())

    return render_template('new_ad.html', **default_kwargs)

