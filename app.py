

from random import randint
from flask import Flask, render_template, request, redirect

app = Flask(__name__)





login_base={
    1 : {'username':'mario', 'password': 'italy'},
    2: {'username' : 'luigi' , 'password': 'italianpizza'}
}
# login for primary stakeholders




@app.route('/')
def menu_page():
    #The main menu
     return render_template('index.html')



@app.route('/login')
def login_page():
    # the login page for admins to log into admin page
    return render_template('login.html')


@app.route('/order')
def order_page():
    # The page where customers and mario can place orders
    return render_template('order.html',orderlist=orderList)

with open('generations.csv', 'w', newline='') as o:
    writer = csv.writer(o)

orderList = []
@app.route('/ordering', methods = ['POST'])
def add_order():
    global orderList
    global lentghOrder
    lentghOrder = len(orderList)
    name = request.form['newname']
    order = request.form['neworder']

    neworder = (name, order)
    with open('orderData.csv', 'w', newline='') as o:
        writer = csv.writer(o)
        writer.writerow(orderList)
    orderList.append(neworder)
    print(neworder)
    print(orderList)
    if lentghOrder > 15:
        orderList.pop(0)

    return redirect('/order')



@app.route('/admin')
# the page for mario and luigi
def admin_page():

    return render_template('admin.html', ovenData = data,orderlist=orderList)


oven_data = {
    "ovenResponse" : 0,
    "countdown"    : 0,
    "time"         : 0,
    "temp"         : 0
}


@app.route('/orderUpdate', methods = ['POST'])
def get_data():
    global oven_data
    receivedData = request.get_json()
    oven_data = {
    "ovenResponse" : receivedData["ovenResponse"],
    "countdown"    : receivedData["countdown"],
    "time"         : receivedData["time"],
    "temp"         : receivedData["temp"]
   }
    
    print(oven_data)
    
    return redirect ('/admin')




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
    
       





    
    

    
