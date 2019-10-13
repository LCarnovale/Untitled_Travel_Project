from flask import render_template, request, redirect

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
@app.route('/book', methods=['GET', 'POST'])
def book_main():
    if request.method == 'POST':
        pass

    return render_template('book.html')

