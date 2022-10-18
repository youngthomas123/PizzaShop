from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def menu_page():
     return render_template('index.html')



@app.route('/sign_up')
def sign_up_page():
    return render_template('signup.html')



@app.route('/login')
def login_page():
    return render_template('login.html')



@app.route('/admin')
def admin_page():
    return render_template('admin.html', ovenData = data)



data = []
@app.route('/orderUpdate', methods = ['POST'])
def get_data():
    receivedData = request.get_json()
    newData = (receivedData['countdown'],
    receivedData['time'],
    receivedData['temp'])

    if len(data) >= 1:
        data.pop(0)
        
    data.append(newData)
    return redirect ('/admin')



login_base={
    1 : {'username':'mario', 'password': 'italy'},
    2: {'username' : 'luigi' , 'password': 'italianpizza'}
}

check_login =False
@app.route('/admin_login', methods = ['POST'])
def admin_login():
    check_login =False
    
    login = request.form
    name =login ['sent_username']
    password = login['sent_password']
    for _ in login_base :
        if(name== login_base[_]['username'] and password == login_base[_]['password']) :
            check_login= True
            break
    if (check_login==True):
        return redirect('/')
    else :
        return redirect('/admin')
    
       





    
    

    
