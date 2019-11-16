from flask import render_template, request, redirect, abort, flash, session, url_for
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
from datetime import datetime

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

'''
Landing page
'''
@app.route('/', methods=['GET', 'POST'])
def home():
    
    if request.method == 'POST':
        try:
            search = request.form.get('search')
            refine = False
            print('Form:', request.form)
            print("getting venues with matching options ")

            beds = request.form.get('beds') or None
            bathrooms = request.form.get('bathrooms') or None
            parking = request.form.get('parking') or None


            found = accSystem.get_like(refine=refine,
                bedCount=f'>={beds}' if beds else None,
                bathCount=f'>={bathrooms}' if bathrooms else None,
                carCount=f'>={parking}' if parking else None,
            )
            refine = True if found else False 
            
            print("Filtering by options:", found)
            
            found = accSystem.get_like(refine=refine,
                name=f'~%{search}%',
                description=f'~%{search}%',
                details=f'~%{search}%',
                join="OR"
            )
            refine = found or False
            
            print("Filtering by search term:", found)
            
            # if search: # TODO: Fix geocoding
            #     lower_left, upper_right = text_bounds.split('+')
            #     lower_left = [float(x) for x in lower_left.split(',')]
            #     upper_right = [float(x) for x in upper_right.split(',')]
            #     print("geocoded area:")
            #     print("        ", upper_right)
            #     print(lower_left)
                
            dates = request.form.get('dates').split(' - ')
            if len(dates) == 2:
                startdate = dates[0]
                enddate = dates[1]
                
                print("Filtering by dates:", accSystem.get_available(startdate, enddate, refine=refine)); refine = True
            else:
                startdate = datetime.today().strftime('%d/%m/%Y')
                enddate = None

            location = request.form.get('geocodedvalue')
            distance = request.form.get('distance')
            if location:
                print("getting venues near", location)
                print(accSystem.get_near(location.split(', '), distance, refine=refine)); refine=True
            # elif text_bounds:
            # TODO: This is a bit dodgy the target location and search term should be separate
            if location: search = None
            results = accSystem.advancedSearch(search, None, None, None, beds,
                                                bathrooms, parking, location, distance)
            results = list(map(accSystem.get_acc, results))
            # print(results[0].get_images())
            return render_template('search_results.html', results = results)
        except db.OperationalError as e:
            return render_template('404.html', err_msg=rf"""Unable to connect to database.
Message: {str(e)}""")

        except Exception as e:
            print('----------------------------------')
            print('INVALID DATA WAS ENTERED TO SEARCH')
            print('Error as follows:')
            print(e)
            print('----------------------------------')
            raise e

        return render_template('search_results.html', results = [])

    return render_template('home.html')

'''
Login page
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
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

        return redirect('/')
    return render_template('login.html')

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
    try:
        acc = accSystem.get_acc(id)
    except Exception as e:
        return render_template('404.html', err_msg=f"""Unable to connect to database.
Message: {str(e)}""")
    if acc == None:
        abort(404)

    if request.method == 'POST':
        '''
        if request.form.get('review_submit') != None:
            if request.form.get('rating_input') not in ['1','2','3','4','5']:
                raise ValueError('Rating not submitted, or form mangled')
            print(request.form.get('review'))
            return redirect(url_for('book_main', id=id))
        '''

        form = request.form
        if 'id' in session:
            bookingSystem.create_booking(
                id, session['id'], 
                datetime.strptime(form['book_start'], "%d/%m/%Y"), 
                datetime.strptime(form['book_end'], "%d/%m/%Y")
            )
            return render_template('book_confirm.html', acc=acc)
        else:
            return render_template('login.html', 
                err_msg = "Please login to make a booking.")

    # Get owner details, address details, availabilities.
    owner = db.owners.get(acc.ownerid)
    address = Address(*db.addresses.get(acc.aid)[1:])
    images = acc.get_images()
    print(images)
	# avails = [[str(x[2]), str(x[3])] for x in db.venues.get_availabilities(id)]
    
    reviews = src.review.get_for_venue(id)

    return render_template('book.html', acc=acc, owner=owner, id=id,
        address=address, reviews = reviews, images = images)


'''
Booking page, accessed via the booking page
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
            f.save(os.path.join('static/'+app.config['UPLOAD_FOLDER'], f.filename))
            print(type(f))
            url = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            db.images.insert(venueid, url)

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

