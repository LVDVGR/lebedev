from flask import Flask, session, redirect, render_template, url_for, request
from functools import wraps
from database_interface import *
import os
from database_engine import employees_session, orders_session, wine_products
from models import Departments, Employees, Clients, OrderTable
## TODO create a separate roads and html documents for client products and admin products

app = Flask(__name__)
app.secret_key = 'qwerty1234'
sessions = {}

def requires_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))

        if not session['admin']:
            return redirect(url_for('products'))

        return f(*args, **kwargs)
    return decorated_function

def requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def auth():
     return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'GET':
          return render_template('login.html')
     if request.method != 'POST': return

     username = request.form['username']
     password = request.form['password']

     result = client_authorize(username, password)

     if not result:
          return render_template('login.html', 
                                 invalid='Incorrect login or password')
     
     session['username'] = username
     session['admin'] = False
     session['logged_in'] = True

     return redirect(url_for('products'))


@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
     if request.method == 'GET':
          return render_template('login_admin.html')
     if request.method != 'POST': return

     username = request.form['username']
     password = request.form['password']

     result =  employee_authorize(username, password)

     if not result:
          return render_template('login.html', invalid='Incorrect login or password')
     
     session['username'] = username
     session['admin'] = True
     session['logged_in'] = True

     return redirect(url_for('manage_employees'))

@app.route('/logout')
def logout():
     session.clear()
     return redirect(url_for('products'))


@app.route('/orders')
def orders():
     if not session.get('username', False):
          return redirect(url_for('login'))
     
     orders = get_my_orders(session['username'])
     total_prices = [sum([(p['price']) * p['amount'] for p in order.order_list.values()]) for order in orders]
     return render_template('wine_orders.html', orders=zip(orders, total_prices), 
                            logged_in=True,
                            username=session.get('username', None),
                            total_prices=total_prices)

@app.route('/order_info')
@requires_auth
def order_info():
     args = request.args
     if not args.get('order_id', default=False):
          return redirect(url_for('products'))
     
     if session['admin'] == True:
          order = get_order_info(None, args.get('order_id'))
          products = [get_product_info(p) for p in order.order_list]
          total_price = sum([(p['price']) * p['amount'] for p in order.order_list.values()])
          return render_template('manage_order.html', order=order, products=products, total_price=total_price)
     
     order = get_order_info(session['username'], args.get('order_id'))
     products = [get_product_info(p) for p in order.order_list]
     total_price = sum([(p['price']) * p['amount'] for p in order.order_list.values()])
     return render_template('order.html', order=order, products=products, total_price=total_price)


@app.route('/products')
def products():
     all_products = wine_products.find()
     return render_template('wine_products.html', products=all_products, 
                            logged_in=session.get('logged_in', False),
                            username=session.get('username', None))

@app.route('/shopping_cart')
def shopping_cart():
     return render_template('wine_shopping_cart.html', 
                            logged_in=session.get('logged_in', False),
                            username=session.get('username', None))

@app.route('/manage_clients')
@requires_admin
def manage_clients():
     clients = orders_session.query(Clients).all()
     return render_template('manage_wine_clients.html', clients=clients,
                            username=session.get('username', None))

@app.route('/mamage_orders')
def manage_orders():
     if not session.get('username', False):
          return redirect(url_for('login'))
     orders = orders_session.query(OrderTable).all()
     return render_template('manage_wine_orders.html', orders=orders, 
                            logged_in=session.get('logged_in', False),
                            username=session.get('username', None))

@app.route('/manage_employees')
@requires_admin
def manage_employees():
     employees = employees_session.query(Employees).all()
     print(session.get('logged_in', False))
     return render_template('manage_wine_employees.html', employees=employees,
                            username=session.get('username', None))

@app.route('/manage_products')
@requires_admin
def manage_products():
     all_products = wine_products.find()
     return render_template('manage_wine_products.html', products=all_products,
                            username=session.get('username', None))

if __name__ == '__main__':
    app.run(debug=True)