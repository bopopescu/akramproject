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


# Decorators #
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap
# End of decorators #


# Routes #
@app.route('/')
def shop_main():
    return render_template('shop-index.html')


@app.route('/item')
def shop_item():
    return render_template('shop-item.html')


@app.route('/product-list')
def shop_product_list():
    return render_template('shop-product-list.html')


@app.route('/contacts')
def shop_contacts():
    return render_template('shop-contacts.html')


@app.route('/account')
@login_required
def shop_account():
    return render_template('shop-account.html')


@app.route('/cart')
def shop_cart():
    return render_template('shop-shopping-cart.html')


@app.route('/faq')
def shop_faq():
    return render_template('shop-faq.html')


@app.route('/about')
def shop_about():
    return render_template('shop-about.html')


@app.route('/tc')
def shop_tc():
    return render_template('shop-contacts.html')


@app.route('/privp')
def shop_privp():
    return render_template('shop-privacy-policy.html')


@app.route('/prod-l-w')
def shop_prod_w():
    return render_template('shop-product-list-women.html')


@app.route('/prod-l-k')
def shop_prod_k():
    return render_template('shop-product-list-Kids.html')


@app.route('/pass-reset')
def shop_pass_reset():
    return render_template('forgot-password.html')

# End of routes #


# Login, logout, and registration #
def retrieve_users():
    records = SQLdb.retrieve_users()
    print(records)
    return records


@app.route('/checkout', methods=['GET', 'POST'])
def shop_checkout():
    users=retrieve_users()
    for user in users:
        print(user[0])
        print(user[1])

    error = None
    if request.method == 'POST':
        if request.form['username'] != users[0] or request.form['password'] != users[1]:
            error = 'Invalid credential. Please, try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('shop_main'))
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

