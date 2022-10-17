from flask import Flask, render_template,request,redirect

app = Flask(__name__)

@app.route('/')
def menu_page():
    return render_template ('index.html')


@app.route('/sign_up')
def sign_up_page():
    return render_template('')

