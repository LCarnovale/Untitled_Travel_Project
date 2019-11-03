from flask import render_template, request, redirect, abort, flash, session, url_for
from flask_login import LoginManager, login_user
from src.accommodation import Accommodation
from src.accommodationSystem import AccommodationSystem
from src.address import Address
from src.user import User
from src.stayDetails import StayDetails
from src.booking import Booking
import src.userSystem as US
import src.accommodationSystem as AS
import src.bookingSystem as BS
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
        try:
            search = request.form.get('search')
            text_bounds = request.form.get('geocodedvalue')
            startdate = request.form.get('startdate')
            enddate = request.form.get('enddate')
            beds = request.form.get('beds')
            bathrooms = request.form.get('bathrooms')
            parking = request.form.get('parking')
            location = request.form.get('location')
            distance = request.form.get('distance')

            if (search or startdate or enddate or beds or
                bathrooms or parking or location):
                print(search, startdate, enddate, beds,
                      bathrooms, parking, location)
                accSystem.get_all_ads()
                results = accSystem.advancedSearch(search, text_bounds, startdate, enddate, beds,
                                                   bathrooms, parking, location, distance)
                return render_template('search_results.html', results = results)
            else:
                accSystem.get_all_ads()
                results = accSystem.advancedSearch(search, text_bounds, startdate, enddate, beds,
                                                   bathrooms, parking, location, distance)
                return render_template('search_results.html', results = results)
        except Exception as e:
            print('----------------------------------')
            print('INVALID DATA WAS ENTERED TO SEARCH')
            print('Error as follows:')
            print(e)
            print('----------------------------------')
            raise e

        return render_template('search_results.html', results = [])

    return render_template('home.html', **default_kwargs)

'''
Login page
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Attempt a Login
        form = request.form
        login_id = -1
        if db.is_connected:
            login_type = form['login_select'] # Will be either 'owner' or 'user'
            result = userSystem.check_user_pass(
                form['username'], form['password'], login_type
            )
            if result is not None:
                login_id = result
                user = userSystem.get_user(
                    login_id, u_type=form['login_select'])  # should be same as  User(*result[1:])
            else:
                return render_template('login.html', login_fail=True)
            session['login_type'] = login_type

        else:
            result = (form['password'] == 'admin' and form['username'] == 'admin')
            if result:
                user = User(
                    "Developer",
                    "admin",
                    "admin@temp.com",
                    "0456123456")
            else:
                print("No database connection, try admin & admin")
        if result:
            session['id'] = login_id
            d = user.todict()
            for k, v in zip(d.keys(), d.values()):
                session[k] = v

        return redirect('/')
    return render_template('login.html', **default_kwargs)

'''
Logout
'''
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove any existing sessions
    session.pop('username', None)
    session.pop('id', None)

    return redirect(url_for('home'))

'''
Signup page
'''
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = request.form
    if request.method == 'POST':
        # Create user.
        try:
            uid = userSystem.create_user(
                form['account_name'],
                form['account_username'],
                form['account_password'],
                form['account_email'],
                form['account_phone'],
                form['account_description']
            )
        except US.UserCreateError as e:
            if e.col == 'userName':
                return render_template('signup.html', username_taken=True)
            if e.col == 'email':
                return render_template('signup.html', invalid_email=True)

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
    # Create user.
    uid = session['id']
    user = userSystem.get_user(uid, u_type=session['login_type'])
    if request.method == 'POST':
        form = request.form

        if user is not None:
            if form['account_pwd_new']:
                pwd_check = userSystem.check_user_pass(
                    user.username, form['account_pwd_current'], u_type=user.type)
                if pwd_check is None:
                    # Incorrect password given
                    return render_template('edit.html', _user=user, pass_fail=True)
                else:
                    # Correct password given
                    user = userSystem.set_password(
                        uid, form['account_pwd_new'], u_type=user.type)
            user.name = form['account_name']
            user.username = form['account_username']
            user.email = form['account_email']
            user.mobile = form['account_phone']
            user.desc = form['account_description']
            
            # Assume edits successful
            d = user.todict()
            for k, v in zip(d.keys(), d.values()):
                session[k] = v
            # session['email'] = user.email
            # session['phone'] = user.phone
            # session['desc'] = user.desc
            userSystem.update_user(uid, u_type=user.type)
        else:
            print("Error user not found")
        return render_template('confirm_edit.html')
    return render_template('edit.html', _user=user)
	
'''
Main Booking page
'''  
@app.route('/book/<id>', methods=['GET', 'POST'])
def book_main(id):

    acc = accSystem.get_acc(id)
    if acc == None:
        abort(404)

    if request.method == 'POST':
        if request.form.get('review_submit') != None:
            if request.form.get('rating_input') not in ['1','2','3','4','5']:
                raise ValueError('Rating not submitted, or form mangled')
            #TODO: post review
            print(request.form.get('review'))
            return redirect(url_for('book_main', id=id))

        form = request.form
        if 'id' in session:
            bookingSystem.create_booking(
                id, session['id'], form['book_start'], form['book_end']
            )
            return render_template('book_confirm.html', acc=acc, **default_kwargs)
        else:
            return render_template('login.html', 
                err_msg = "Please login to make a booking.", **default_kwargs)

    # Get owner details, address details, availabilities.
    owner = db.get_owner(acc.ownerid)
    address = Address(*db.get_address(acc.aid)[1:])
    # avails = [[str(x[2]), str(x[3])] for x in db.get_venue_availabilities(id)]
    
    return render_template('book.html', acc=acc, owner=owner, 
        address=address, **default_kwargs)



'''
Main Post accommodation page
'''  
@app.route('/post_ad', methods=['GET', 'POST'])
def ad_main():
    if request.method == "POST":
        form = request.form
        

        # Find owner:
        # (We haven't asked for enough info, pick a test owner)
        owner = db.get_owner(1)
        # Create Address info:
        lat, lng = form['acc_location'].split(",")
        lat = lat.strip()[:10]
        lng = lng.strip()[:10]
        aid = db.insert_address(form['acc_addr'], lat, lng)

        # Send to accommodationSystem
        venueid = accSystem.create_accomodation(
            int(owner[0]),         int(aid),               form['acc_name'], 
            int(form['acc_nbed']), int(form['acc_nbath']), int(form['acc_ncar']), 
            form['acc_details'],   float(form['price']),   int(form['min_stay']), 
            int(form['max_stay']), form['details']
        )

        # Create associated date ranges
        # This could be moved to another module?

        for i in range(0, int(form['dateCount']), 2):
            db.insert_availability(
                venueid, form[f'dateRange_{i}'], form[f'dateRange_{i+1}']
            )
        # Done
        # print(request.form['avail_date'])
        return render_template('ad_confirm.html', id=venueid, **default_kwargs)

    return render_template('new_ad.html', **default_kwargs)

