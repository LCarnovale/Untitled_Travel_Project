from flask import render_template, request, redirect, abort, flash, session, url_for
from flask_login import LoginManager, login_user
from src.accommodation import Accommodation
from src.accommodationSystem import AccommodationSystem
from src.address import Address
from src.user import User
from src.stayDetails import StayDetails
import src.userSystem
from server import accSystem
from server import userSystem
from server import bookingSystem
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
        login_id = -1
        if db.is_connected:
            result = db.check_user_pass(request.form['username'], request.form['password'])
            if result is None:
                print("Login failed")
            else:
                print(f"Log in for {result[1]} ({result[2]}) successful.")
                login_id = result[0]
                user = User(*result[1:])
        else:
            result = (request.form['password'] == 'admin' and request.form['username'] == 'admin')
            if result:
                print("Logged in as admin")
                user = User(
                    "Developer",
                    "admin",
                    "admin@temp.com",
                    "0456123456")
            else:
                print("Try admin & admin")
        if result:
            session['name'] = user.name
            session['username'] = user._username
            session['email'] = user._email
            session['mobile'] = user._mobile
            session['id'] = login_id
            session['desc'] = user._desc
        print(session['mobile'])
        return render_template('home.html')
    return render_template('login.html')

'''
Logout
'''
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove any existing sessions
    print(session)
    session.pop('username', None)
    session.pop('id', None)

    return redirect(url_for('home'))

'''
Signup page
'''
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Create user.
        form = request.form
        uid = userSystem.create_user(
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
Edit profile page
'''
@app.route('/edit', methods=['GET', 'POST'])
def editprofile():
    if request.method == 'POST':
        # Create user.
        form = request.form
        uid = userSystem.get_user(session['id'])

        if uid is not None:
            user._email = form['account_email']
            user._phone = form['account_phone']
            user._desc = form['account_description']
        else:
            print("Error user not found")
        return render_template('confirm_edit.html')
    return render_template('edit.html')
	
'''
Main Booking page
'''  
@app.route('/book/<id>', methods=['GET', 'POST'])
def book_main(id):
    acc = accSystem.get_acc(id)
    if acc == None:
        abort(404)

    if request.method == 'POST':
        form = request.form
        if session['id']:
            bookingSystem.create_booking(
                id, session['id'], form['book_start'], form['book_end']
            )

    return render_template('book.html', acc=acc, **default_kwargs)



'''
Main Post accommodation page
'''  
@app.route('/post_ad', methods=['GET', 'POST'])
def ad_main():
    if request.method == "POST":
        form = request.form
        # form elements:
        # acc_name
        # acc_addr
        # acc_nbed
        # acc_nbath
        # acc_ncar
        # acc_details
        # acc_location
        # own_name
        # own_email
        # own_phone
        # description
        # price
        # dateCount 
        # dateRange_0
        # dateRange_1 ... (up to dateCount - 1)
        # min_stay
        # max_stay
        # details

        # Find owner:
        # (We haven't asked for enough info, pick a test owner)
        owner = db.get_owner(1)
        # Create Address info:
        aid = db.insert_address(form['acc_location'])

        # Send to accommodationSystem
        venueid = accSystem.create_accomodation(
            int(owner[0]),         int(aid),               form['acc_name'], 
            int(form['acc_nbed']), int(form['acc_nbath']), int(form['acc_ncar']), 
            form['description'],   float(form['price']),   int(form['min_stay']), 
            int(form['max_stay']), form['details']
        )

        # Create associated date ranges
        # This could be moved to another module?
        for i in range(0, int(form['dateCount']), 2):
            newav = db.insert_availability(
                venueid, form[f'dateRange_{i}'], form[f'dateRange_{i+1}']
            )

        # Done

        return render_template('ad_confirm.html', id=venueid, **default_kwargs)

    return render_template('new_ad.html', **default_kwargs)

