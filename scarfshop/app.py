from __future__ import print_function
import json
import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, url_for, redirect, session
from jinja2 import Template
import SQLdb


app = Flask(__name__)
# app = Flask(__name__, template_folder='/scarfshop/templates', static_url_path='/scarfshop/static')
app.secret_key = 'AD83nsod3#Qo,c0e3n(CpamwdiN"Lancznpawo.j3eOMAPOM;CAXMALSMD343644'
app.jinja_env.filters['zip']=zip


def pull_sqldb(product_id):
    return SQLdb.get_product_by_id(product_id)


# Decorators #
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap



#
# @app.context_processor
# def utility_processor():
#     def pull_sqldb(product_id):
#         return SQLdb.get_product_by_id(product_id)
#
#     return dict(pull_sqldb=pull_sqldb)
#     #return productID
# End of decorators #


# Routes #
@app.route('/', methods=['GET', 'POST'])
def shop_main():
    cart_items = SQLdb.get_cart_details()
    print(cart_items)
    temp_list=[]
    for cart_item in cart_items:
        temp_list.append(SQLdb.get_product_by_id(cart_item[0]))
    print(temp_list)
    return render_template('shop-index.html', items=cart_items,t_items=temp_list)


@app.route('/item')
def shop_item():
    cart_items = SQLdb.get_cart_details()

    return render_template('shop-item.html', items=cart_items)


@app.route('/product-list')
def shop_product_list():
    cart_items = SQLdb.get_cart_details()

    return render_template('shop-product-list.html', items=cart_items)


@app.route('/contacts')
def shop_contacts():
    cart_items = SQLdb.get_cart_details()
    return render_template('shop-contacts.html', items=cart_items)


@app.route('/account')
@login_required
def shop_account():
    cart_items = SQLdb.get_cart_details()
    return render_template('shop-account.html', items=cart_items)


@app.route('/cart')
def shop_cart():

    cart_items=SQLdb.get_cart_details()

    return render_template('shop-shopping-cart.html',items=cart_items)


@app.route('/faq')
def shop_faq():
    cart_items = SQLdb.get_cart_details()
    return render_template('shop-faq.html', items=cart_items)


@app.route('/about')
def shop_about():
    cart_items = SQLdb.get_cart_details()
    return render_template('shop-about.html', items=cart_items)


@app.route('/tc')
def shop_tc():
    cart_items = SQLdb.get_cart_details()
    return render_template('shop-contacts.html', items=cart_items)


@app.route('/privp')
def shop_privp():
    cart_items = SQLdb.get_cart_details()
    return render_template('shop-privacy-policy.html', items=cart_items)


@app.route('/prod-l-w')
def shop_prod_w():
    cart_items = SQLdb.get_cart_details()
    return render_template('shop-product-list-women.html', items=cart_items)


@app.route('/prod-l-k')
def shop_prod_k():
    cart_items = SQLdb.get_cart_details()
    return render_template('shop-product-list-Kids.html', items=cart_items)


@app.route('/pass-reset')
def shop_pass_reset():
    cart_items = SQLdb.get_cart_details()
    return render_template('forgot-password.html', items=cart_items)

# End of routes #


# Login, logout, and registration #
@app.route('/checkout', methods=['GET', 'POST'])
# source: https://codeshack.io/login-system-python-flask-mysql/#creatingtheloginsystem
def shop_checkout():
    error = None
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        user_username = request.form['username']
        user_password = request.form['password']
        user_retrieved = SQLdb.get_users(user_username, user_password)

        if user_retrieved:
            # query: cursor.execute('SELECT * FROM tblCustomer WHERE email = %s AND password = %s', ('as', 'as'))
            #is None for invalid password username

            # query: cursor.execute('SELECT * FROM tblCustomer WHERE email = %s AND password = %s', ('andrew.clarkson@yahoo.com', 'password2'))
            # is account is: ('andrew.clarkson@yahoo.com', 'password2', 'Andrew', 'Johnson', datetime.date(1984, 10, 3)) for retrieved
            session['logged_in'] = True
            session['id'] = user_retrieved['id']
            session['username'] = user_retrieved['email']
            return redirect(url_for('shop_main'))
        else:
            error = 'Invalid credentials. Please, try again.'
    return render_template('shop-checkout.html', error=error)



@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.clear()
    return redirect(url_for('shop_main'))


@app.route('/registration')
def registration():
    return render_template('registration.html')



# End of login and registration #




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8089)

