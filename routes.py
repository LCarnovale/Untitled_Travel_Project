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
@app.route('/book/<id>', methods=['GET', 'POST'])
def book_main(id):
    if request.method == 'POST':
        pass #TODO
        return render_template('book_confirm.html')

    return render_template('book.html')


'''
Main Post accommodation page
'''  
@app.route('/post_ad', methods=['GET', 'POST'])
def ad_main():
    if request.method == 'POST':
        pass #TODO
        return render_template('ad_confirm.html', ad_id = 0)

    return render_template('new_ad.html')

