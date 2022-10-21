from random import randint
from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)


data = []
# oven data



app.route('/wrong')
def wrong_username():
    return render_template('wrong.html')


@app.route('/order')
def order_page():
    # The page where customers and mario can place orders
    return render_template('order.html',orderlist=orderList)
    
    return render_template('order.html',orderlist=orderlist)



with open('generations.csv', 'w', newline='') as o:
    writer = csv.writer(o)

orderList = []
@app.route('/wrong_login')
def wrong_logon_page():
    return render_template('wrong.html')




order = []
orderlist = []
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

    global order, orderlist
      
    received_data = request.form["pizza"]
    if (received_data !="complete") : 
        order.append(received_data)
        print (order)
    else : 
        unique= str(randint(100, 999))
        order.insert(0,{"order_id" : unique})
        orderlist.append(order)
        order = []
        print (order)
        print(orderlist)

    print (orderlist)
    
    return redirect('/order')


@app.route('/admin')
# the page for mario and luigi
def admin_page():
    return render_template('admin.html', oven_data=oven_data,orderlist=orderlist)


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
    newData = (receivedData['ovenResponse'],
    receivedData['countdown'],
    receivedData['time'],
    receivedData['temp'])
    print (receivedData)
    print(newData)
    print(data)

    if len(data) >= 1:
        data.pop(0)
        
    data.append(newData)
    oven_data = {
    "ovenResponse" : receivedData["ovenResponse"],
    "countdown"    : receivedData["countdown"],
    "time"         : receivedData["time"],
    "temp"         : receivedData["temp"]
   }
    
    print(oven_data)
    
    return redirect ('/admin')


    if (check_login==True):
        return redirect('/admin')
    else :
        return redirect('/wrong')
        return redirect('/wrong_login')

    
       





    
    

    
