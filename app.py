
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
    
    return render_template('order.html',orderlist=orderlist)




@app.route('/wrong_login')
def wrong_logon_page():
    return render_template('wrong.html')




order = []
orderlist = []
orderque = []
@app.route('/ordering', methods = ['POST'])
def add_order():
    global order, orderlist,orderque
      
    received_data = request.form["pizza"]
    if (received_data !="complete") : 
        order.append(received_data)
        print (order)
    else : 
        unique= str(randint(100, 999))
        order.insert(0,{"order_id" : unique})
        orderlist.append(order)
        orderque.append(order)
        order = []
        print (order)
        print(orderlist)

    print (orderlist)
    
    return redirect('/order')



@app.route('/admin')
# the page for mario and luigi
def admin_page():
    return render_template('admin.html', oven_data=oven_data,completedOrder=completedOrder,orderque=orderque)



oven_data = {
    "ovenResponse" : 0,
    "countdown"    : 0,
    "time"         : 0,
    "temp"         : 0,
    "orderid"      :'',
    "order"        :''
}

i = 0
completedOrder=[]
@app.route('/orderUpdate', methods = ['POST'])
def get_data():
    global oven_data,orderlist,i,completedOrder,orderque
    receivedData = request.get_json()
    oven_data = {
    "ovenResponse" : receivedData["ovenResponse"],
    "countdown"    : receivedData["countdown"],
    "time"         : receivedData["time"],
    "temp"         : receivedData["temp"],
    "orderid"      : orderlist[i][0]["order_id"],
    "order"        : orderlist[i][1:]
   }
    if(oven_data["ovenResponse"]=="Pizza is ready"):
        
        completedOrder.append(orderlist[i])
        orderque.pop(0)
        
        i=i+1
        print (i)

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
        return redirect('/admin')
    else :
        return redirect('/wrong_login')
    
       





    
    

    
