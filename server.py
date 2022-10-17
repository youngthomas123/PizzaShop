from flask import Flask, render_template,request,redirect

app = Flask(__name__)

@app.route('/')
def menu_page():
    return render_template ('menu.html')

