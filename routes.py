from flask import render_template, request, redirect
from src.accommodation import Accommodation
from src.accommodationSystem import AccommodationSystem
from src.address import Address
from src.user import User
from src.stayDetails import StayDetails
from server import accSystem
from server import userSystem
from server import app


'''
Landing page
'''
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pass

    return render_template('base.html')


'''
Main Booking page
'''  
@app.route('/book/<id>', methods=['GET', 'POST'])
def book_main(id):
    acc = accSystem.getAcc(id)
    print(acc)
    if request.method == 'POST':
        pass #TODO

    return render_template('book.html', acc=acc)



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
        stay = StayDetails(request.form['price'], request.form['avail_start'],
                        request.form['avail_end'], request.form['min_stay'],
                        request.form['max_stay'], request.form['stay_details'])
        # Make an accommodation class
        acc = Accommodation(request.form['acc_name'], addr,
                        request.form['acc_nbed'], request.form['acc_nbath'],owner, stay, request.form['acc_details'],)
        # Add the accommodation into the system
        accSystem.addAcc(acc)
        # Add the user into the system
        userSystem.addUser(owner)
        return render_template('ad_confirm.html', id=acc.getID())

    return render_template('new_ad.html')

