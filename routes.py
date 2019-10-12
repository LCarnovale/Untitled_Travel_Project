from flask import render_template, request, redirect

from server import app

'''
Landing page
'''
@app.route('/', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        pass

    return render_template('index.html')