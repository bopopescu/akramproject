import os
import re
import mysql.connector
from mysql.connector import Error
from flask import redirect

db_username = os.environ['USERNAME']
db_password = os.environ['PASSWORD']
database = os.environ['DATABASE']
host = os.environ['HOST']
port = '37306'


def delete_cart_entry(productID):
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password,port=port)
        cursor = connection.cursor()
        delquery='DELETE FROM tblGuestCart WHERE productID = '+str(productID)
        cursor.execute(delquery)
        connection.commit()
    except Error as e:
        print( 'Error deleting cart item')

def add_product_to_cart(product):
    cart_product=product[0],1,product[2]
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password,port=port)
        cursor = connection.cursor()
        query='INSERT INTO tblGuestCart () VALUES '+str(cart_product)
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print( 'Error adding product to cart')


def update_cart(productID,quantity):
    prod_details = get_product_by_id(productID)
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password,port=port)
        cursor = connection.cursor()
        query='UPDATE tblGuestCart SET quan = '+str(quantity)+' WHERE productID = '+str(productID)
        cursor.execute(query)

        price=float(prod_details[2])
        total=round(price*quantity,2)
        query2='UPDATE tblGuestCart SET total = '+str(total)+' WHERE productID = '+str(productID)
        cursor.execute(query2)
        cursor.execute('SELECT * FROM tblGuestCart')

        c=cursor.fetchall()

        connection.commit()

        print(str(c))
    except Error as e:
        print( 'Error updating cart')


def get_cart_details():
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password,port=port)
        print(connection)
        cursor = connection.cursor()
        print(cursor)
        cursor.execute('SELECT * FROM tblGuestCart')
        cart_details = cursor.fetchall()
        print(cart_details)
        return cart_details
    except Error as e:
        print( 'Error getting cart info')


def get_product_by_id(ProductID):
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password,port=port)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tblProduct')
        product_details = cursor.fetchall()

        for prod in product_details:
            if prod[0]==int(ProductID):
                details=prod
        return  details
    except Error as e:
        print( 'Error getting product info')

def get_all_products():
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password,port=port)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tblProduct')
        product_list = cursor.fetchall()
        return product_list
    except Error as e:
        print( 'Error getting product list')

def get_users(user_email, user_password):
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password, port=port)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tblCustomer WHERE email = %s AND password = %s', (user_email, user_password))
        account = cursor.fetchone()
        return account

    except Error as e:
        print("Error while connecting to MySQL.", e)

    finally:
        try:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        except Error as e:
            print("No connection exists to the MySQL server.", e)


def registeruser(firstname, lastname, email, telephone, password, address1, address2, city, postcode, country):
    try:
        message = ""
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password, port=port)
        cursor = connection.cursor()

        # Source of solution: https://stackoverflow.com/a/46020475
        query = """SELECT * FROM tblCustomer WHERE (email) = (%s)"""
        # query = ('SELECT * FROM tblCustomer WHERE email = %s', email)
        cursor.execute(query, (email,))

        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', firstname):
            message = 'First name must contain only characters!'
        elif not re.match(r'[A-Za-z0-9]+', lastname):
            message = 'Last name must contain only characters and numbers!'
        elif not any([firstname, lastname, email, telephone, password, address1, city, postcode, country]):
            message = 'Please fill out the form!'
        else:
            # tblCustomers ( email, password, firstname, lastname, dob, userID )
            cursor.execute('INSERT INTO tblCustomer VALUES (%s, %s, %s, %s, NULL)', (email, password, firstname, lastname)) #todo: NULL vs ""
            connection.commit()

            #tblAddress ( streetname, streetnumber, postcode, city, country, email, telephone )
            cursor.execute('INSERT INTO tblAddress VALUES (%s, %s, %s, %s, %s, %s, %s )', (address1, address2, postcode, city, country, email, telephone))
            connection.commit()

            message = 'You have successfully registered!'
            print("User registered")
            return message

    except Error as e:
        print("Error encountered", e)
        return "Error encountered."

    finally:
        try:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        except Error as e:
            print("No connection exists to the MySQL server.", e)


def retrieve_address():
    try:
        connection = mysql.connector.connect(host=host, database=database, user=db_username, password=db_password, port=port)
        sql_select_Query = "select * from tblAddress"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchone()
        print("Total number Addresses: ", cursor.rowcount)
        print("\nPrinting each Address record")

        for row in records:
            print("Streetname= ", row[0], )
            print("Streetno = ", row[1])
            print("postcode  = ", row[2])
            print("city  = ", row[3])
            print("country  = ", row[4])
            print("email = ", row[5])
            print("phoneNo  = ", row[6], "\n")

        return records

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


#