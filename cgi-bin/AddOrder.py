#!/usr/bin/env python3

print('Content-Type:text/html')
print("")

import mysql.connector
from mysql.connector import Error
import cgi
import cgitb

cgitb.enable(display=0, logdir="/logs")
input_data=cgi.FieldStorage()
conn = None
cursor = None

def checkTableExists(conn, tablename):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM hen.tables WHERE table_name = '{0}'".format(tablename))
    if cursor.fetchone()[0] == 1:
        cursor.close()
        return True
    cursor.close()
    return False

product_insert_stmt = ("INSERT INTO product(name, price)""VALUES(%s, %d)")
products = [('Full Package', 150), ('Simple Package', 100), ('Partial Package', 80), ('The Basics', 70)]
profile_script_1 = '''
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="canonical" href="https://html5-templates.com/" />
        <title>Hen Events</title>
        <meta name="description" content="Hen Events">
        <link rel="stylesheet" href="/WebContent/styles/style.css" />
        <script src="/WebContent/scripts/script.js"></script>
    </head>

    <body>
        <header>
            <div id="logo"><img src="/WebContent/images/flower-logo.png">Hen Events</div>
            <nav>  
                <ul>
                    <li><a href="/">Home</a>
                    <li><a href="/WebContent/services.html">Services</a>
                    <li><a href="/WebContent/booking.html">Booking</a>
                    <li><a href="/WebContent/about.html">About</a>
                    <li><a href="/WebContent/profile.html">Profile</a>
                </ul>
            </nav>
        </header>
        <section>
            <strong>Profile</strong>
        </section>
        <section id="pageContent">
            <div class="card rounded">'''

profile_script_2 = '''
    </div>
	</section>
	<footer>
		<p>&copy; 2020 by Hen Events | 3607 Trousdale Pkwy Los Angeles, CA 90089 | info@henevents.com</p>
	</footer>
</body>'''
print(profile_script_1)
error = False
try:
    conn = mysql.connector.connect(host='localhost',
                                   user='root',
                                   password='password')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS hen")
        cursor.execute("USE hen")
        if not checkTableExists(conn, 'products'):
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    product_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(30)  NOT NULL,
                    price INT(3) NOT NULL)
                ''')
            for product in products:
                cursor.execute(product_insert_stmt, product)
            conn.commit()
        if not checkTableExists(conn, 'orders'):
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INT(6) NOT NULL AUTO_INCREMEMNT PRIMARY KEY,
                    user_id INT(6) NOT NULL,
                    product_id INT(6) NOT NULL,
                    date VARCHAR(10) NOT NULL,
                    time VARCHAR(10) NOT NULL,
                    pay_status INT(1) NOT NULL,
                    CONSTRAINT 'user_id' FOREIGN KEY (user_id) REFERENCES user(user_id),
                    CONSTRAINT 'product_id' FOREIGN KEY (product_id) REFERENFES product(product_id))
                    ''')
        try:
            try:
                fname = input_data["fname"].value
                lname = input_data["lname"].value
                email = input_data["email"].value
                password = input_data["password"].value
                confpassword = input_data["confpassword"].value
                if password == confpassword:
                    cursor.execute("SELECT * FROM users WHERE email='" + input_data["email"].value + "'")
                    if cursor.fetchone() is not None:
                        print("<p>A user with that email already exists</p>")
                        error = True
                    else:
                        cursor.execute("INSERT INTO users (fname, lname, email, pw) VALUES ('" + fname + "', '" + lname + "', '" + email + "', '" + password + "')" )
                        conn.commit()
                        print("<p>Hello {0} {1}!</p>".format(fname, lname))
                        print("<p>Your email is: {0}</p><br>".format(email))
                        print("<p><a href='/'><button type='button' class='button'>Logout</button></a></p>")
                else:
                    print("<p>Passwords do not match</p>")
                    error = True
            except KeyError as ke:
                print("<p>Form values cannot be blank!</p>")
                error = True
            except Error as e:
                print("<p>", e, "</p>")
            finally:
                cursor.close()
        except Error as e:
                print("<p>Error reading the form</p>")
                error = True
    else:
        print('<p>Unable to connect to MySQL database</p>')
        error = True
except Error as e:
    print('<p>',e,'</p>')
    error = True
finally:
    if conn is not None and conn.is_connected():
        conn.close()
    if error == True:
        print("<br><p><a href='/WebContent/register.html'><button type='button' class='button'>Return to Registration</button></a></p>")
    print(profile_script_2)