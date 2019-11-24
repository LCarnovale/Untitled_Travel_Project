from flask import render_template, request, redirect, abort, flash, session, url_for, g
from flask_login import LoginManager, login_user
from src.accommodation import Accommodation
from src.accommodationSystem import AccommodationSystem
from src.address import Address
from src.user import User
from src.stayDetails import StayDetails
from src.booking import Booking
import src
import src.userSystem as US
import src.accommodationSystem as AS
import src.bookingSystem as BS
from server import accSystem
from server import userSystem
from server import bookingSystem
from server import app
import db
import os
from datetime import datetime, timedelta, date

@app.template_filter('pluralise')
def pluralise(num, singular='', plural='s'):
    if num == 1:
        return f"{num} {singular}"
    else:
        return f"{num} {plural}"

app.add_template_global(f=date.today(), name='today')
# def today():
#     return date.today()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html')


'''
Landing page
'''
@app.route('/', methods=['GET', 'POST'])
def home():
    
    if request.method == 'POST':
        try:
            keyword = request.form.get('keyword')
            refine = False

            beds = request.form.get('beds') or None
            bathrooms = request.form.get('bathrooms') or None
            parking = request.form.get('parking') or None


            found = accSystem.get_like(refine=refine,
                bedCount=f'>={beds}' if beds else None,
                bathCount=f'>={bathrooms}' if bathrooms else None,
                carCount=f'>={parking}' if parking else None,
            )
            refine = True if found else False 
            
            found = accSystem.get_like(refine=refine,
                name=f'~%{keyword}%',
                description=f'~%{keyword}%',
                details=f'~%{keyword}%',
                join="OR"
            )
            refine = found or False
            
            dates = request.form.get('dates').split(' - ')
            if len(dates) == 2:
                startdate = dates[0]
                enddate = dates[1]
                accSystem.get_available(startdate, enddate, refine=refine)
                refine = True
            else:
                startdate = datetime.today().strftime('%d/%m/%Y')
                enddate = None

            location = request.form.get('geocodedvalue')
            distance = request.form.get('radiusval')
            if location:
                accSystem.get_near(location.split(', '), distance, refine=refine)
                refine=True
            # elif text_bounds:
            # TODO: This is a bit dodgy the target location and search term should be separate
            # if location: search = None
            search = request.form['keyword']
            results = accSystem.advancedSearch(search, None, None, None, beds,
                                               bathrooms, parking, location, distance)
            results = accSystem.get_acc(results)
            return render_template('search_results.html', results = results)
        except db.OperationalError as e:
            return render_template('404.html', err_msg=rf"""Unable to connect to database.
Message: {str(e)}""")

        except Exception as e:
            raise e

        return render_template('search_results.html', results = [])

    return render_template('home.html')

'''
Login page
'''
@app.route('/login/', methods=['GET', 'POST'])
@app.route('/login/<send_to>', methods=['GET', 'POST'])
def login(uid=None, u_t='user', send_to='/'):
    if uid is not None:
        # Log them in in the background
        user = userSystem.get_user(uid, u_t)
        session['login_type'] = u_t
        session['id'] = uid
        d = user.todict()
        for k, v in zip(d.keys(), d.values()):
            session[k] = v
        return True
    
    if r'%' in send_to:
        send_to = send_to.replace(r'%', '/')

    if request.method == 'POST':
        # Attempt a Login
        form = request.form
        login_id = -1
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
        if result:
            session['id'] = login_id
            d = user.todict()
            for k, v in zip(d.keys(), d.values()):
                session[k] = v

        return redirect(send_to)
    return render_template('login.html')

'''
Logout
'''
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove any existing sessions
    session.pop('username', None)
    session.pop('id', None)
    session['login_type'] = None

    return redirect(url_for('home'))

'''
Manage ads
'''
@app.route('/manage', methods=['GET', 'POST'])
def manage():
    ads = accSystem.get_for_owner(session['id'])
    return render_template('search_results.html', results=ads, reason='owner_ads')

'''
Owner Signup
'''
@app.route('/signup/owner', methods=['GET', 'POST'])
def signup_owner():
    if request.method == 'POST':
        form = request.form
        name = form['name_input']
        uname = form['uname_input']
        pwd = form['password_input']
        email = form['email_input']
        phone = form['phone_input']
        desc = form['desc_input']

        # TODO: validate input.

        try:
            uid = userSystem.create_owner(
                name, uname, pwd, email, phone, desc
            )
        except Exception as e:
            # TODO: Return errors properly
            print(e)
            return render_template('signup_owner.html', err_msg=str(e))
        else:
            login(uid, 'owner')
            return redirect('/')


    return render_template('signup_owner.html')


'''
Signup page
'''
@app.route('/signup/user', methods=['GET', 'POST'])
def signup():
    form = request.form
    if request.method == 'POST':
        # Create user.
        try:
            uid = userSystem.create_user(
                form['name_input'],
                form['uname_input'],
                form['password_input'],
                form['email_input'],
                form['phone_input'],
                form['desc_input']
            )
        except US.UserCreateError as e:
            if e.col == 'userName':
                return render_template('signup.html', username_taken=True)
            if e.col == 'email':
                return render_template('signup.html', invalid_email=True)
        if uid is not None:
            print("User successfully added.")
            login(uid)
            return redirect('/')
        else:
            print("User insert failed.")
            return render_template('signup.html', err_msg="User signup failed.")
        


    return render_template('signup.html')

'''
Edit profile page
'''
@app.route('/edit', methods=['GET', 'POST'])
def editprofile():
    # Create user.
    try:
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
                abort(500)
            return render_template('confirm_edit.html')
    except Exception as e:
        abort(500)
    return render_template('edit.html', _user=user)


'''
View Bookings page
'''
@app.route('/bookings/', methods=['GET'])
def view_bookings():
    if request.method == 'GET':
        # get current user
        user  = userSystem.get_user(session['id'])
        bookings = user.get_bookings()
        if len(bookings) > 3:
            # reorder to appear as increasing left to right by date
            bookings = [
                *bookings[0::3],
                *bookings[1::3],
                *bookings[2::3]
            ]
        return render_template('view_bookings.html',
                               bookings=bookings, ac=accSystem)

'''
View Bookings for a venue
'''
@app.route('/bookings/<venue_id>', methods=['GET', 'POST'])
def owner_view_bookings(venue_id):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        # get the venue
        venue = accSystem.get_acc(venue_id)
        if int(session['id']) != venue.ownerid:
            abort(404) # You don't own this accommodation

        return render_template('view_bookings.html',
                               bookings=venue.get_bookings(), ac=accSystem,
                               reason="owner", acc = venue, us = userSystem)

'''
Main Booking page
'''  
@app.route('/book/<id>', methods=['GET', 'POST'])
def book_main(id):
    try:
        acc = accSystem.get_acc(id)
    except Exception as e:
        return render_template('404.html', err_msg=f"""Unable to connect to database.
Message: {str(e)}""")
    if acc == None:
        abort(404)

    # Get owner details, address details, availabilities.
    owner = userSystem.get_owner(acc.ownerid)
    address = acc.address
    images = acc.get_images()
    reviews = acc.reviews

    kwargs = {'acc': acc, 'owner': owner, 'id':id,
        'address':address, 'images':images, 'reviews':reviews}

    if request.method == 'POST':
        form = request.form
        if 'id' in session:
            try:
                bid = bookingSystem.create_booking(
                    id, session['id'], 
                    datetime.strptime(form['book_start'], "%d/%m/%Y"), 
                    datetime.strptime(form['book_end'], "%d/%m/%Y")
                )
                booking = bookingSystem.get_booking(bid)
            except ValueError as e:
                print("*** Booking date error: ***")
                print(e)
                return render_template('book.html', booking_fail="Please enter a valid date range using the calendar.", **kwargs)
            except BS.BookingError as e:
                print("*** Booking failed, error: ***")
                print(e)
                return render_template('book.html', **kwargs, 
                    booking_fail=e.msg)

            return render_template('book_confirm.html', booking=booking, **kwargs)
        # else:
        #     global send_to
        #     send_to = url_for('book_main', id=id)
    
    return render_template('book.html', **kwargs)


'''
Review page, accessed via the booking page
'''
@app.route('/review/<id>', methods = ['GET', 'POST'])
def review(id):

    acc = accSystem.get_acc(id)
    if acc == None:
        abort(404)

    if request.method == 'POST':
        print(request.form)
        reccommend = True if request.form.get('recc') == 'yes' else False
        issues = request.form.get('issues')
        good = request.form.get('good')

        db.reviews.insert(id, session['id'], datetime.today(),
                          reccommend, issues, good)

        return redirect(url_for('book_main', id=id))


    return render_template('review.html')

'''
Main Post accommodation page
'''  
@app.route('/post_ad', methods=['GET', 'POST'])
def ad_main():
    if request.method == "POST":
        form = request.form
        # Find owner:
        # (We haven't asked for enough info, pick a test owner)
        if session['login_type'] == 'owner':
            owner = db.owners.get(session['id'])
        else:
            #TODO we should either fix owner signup or have this.
            return render_template('/login', err_msg="Please login as an owner.") 
        
        # Create Address info:
        lat, lng = form['acc_location'].split(",")
        lat = lat.strip()[:10]
        lng = lng.strip()[:10]
        aid = db.addresses.insert(form['acc_addr'], lat, lng)

        # Send to accommodationSystem
        venueid = accSystem.create_accomodation(
            int(owner[0]),         int(aid),               form['acc_name'], 
            int(form['acc_nbed']), int(form['acc_nbath']), int(form['acc_ncar']), 
            form['acc_details'],   float(form['price']),   int(form['min_stay']), 
            int(form['max_stay']), form['details']
        )

        print(request.files)
        for i in (request.files):
            f = request.files[i]
            if not f: continue 
            dir = 'static/'+app.config['UPLOAD_FOLDER']
            f.save(os.path.join(dir, f.filename))
            print(type(f))
            url = os.path.join(dir, f.filename)
            db.images.insert(venueid, '../' + url)

        # Create associated date ranges
        # This could be moved to another module?

        for i in range(0, int(form['dateCount'])):
            start, end = form[f'dateRange_{i}'].split(' - ')
            start = datetime.strptime(start, r'%d/%m/%Y')
            end   = datetime.strptime(end,   r'%d/%m/%Y')
            db.availabilities.insert(
                venueid, start, end
            )
        # Done
        return render_template('ad_confirm.html', id=venueid)

    return render_template('new_ad.html')

