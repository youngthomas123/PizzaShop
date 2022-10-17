from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def menu_page():
     return render_template('admin.html', ovenData = data)



@app.route('/sign_up')
def sign_up_page():
    return render_template('signup.html')



@app.route('/login')
def login_page():
    return render_template('login.html')



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



   
