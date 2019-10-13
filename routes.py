from flask import render_template, request, redirect
from accommodation import Accommodation
from accommodation_system import AccommodationSystem
from server import system
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
    acc = system.getAcc(id)
    print(acc)
    if request.method == 'POST':
        pass #TODO
        acc.book()
        
        return render_template('book_confirm.html')

    return render_template('book.html', acc_name=acc.name,
                           acc_addr=acc.addr)


'''
Main Post accommodation page
'''  
@app.route('/post_ad', methods=['GET', 'POST'])
def ad_main():
    if request.method == "POST":
        pass #TODO
        acc = Accommodation(request.form['acc_name'], request.form['acc_addr'])
        system.addAcc(acc)
        return render_template('ad_confirm.html', id=acc.id)

    return render_template('new_ad.html')

