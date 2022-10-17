from flask import Flask, render_template, request, redirect

app = Flask(__name__)


data = []
@app.route('/admin', methods = ['POST'])
def get_data():
    receivedData = request.get_json()
    newData = (receivedData['countdown'],
    receivedData['time'],
    receivedData['temp'])

    if len(data) >= 15:
        data.pop(0)
        
    data.append(newData)
    return redirect('/')

@app.route('/')
def index():

    return render_template("admin.html", ovenData = data)
