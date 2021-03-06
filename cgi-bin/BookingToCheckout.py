#!/usr/bin/env python3

print('Content-Type:text/html')
print("")

import mysql.connector
from mysql.connector import Error
import cgi
import cgitb
import traceback

cgitb.enable(display=0, logdir="/logs")
input_data=cgi.FieldStorage()
conn = None
cursor = None

login_script = '''
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hen Events</title>
        <meta name="description" content="Hen Events">
        <link rel="stylesheet" href="/WebContent/styles/style.css" />
        <script src="/WebContent/scripts/script.js"></script>
        <link rel="shortcut icon" href="/WebContent/images/flower-logo.png" type="image/png"/>
        <link rel="icon" href="/WebContent/images/flower-logo.png" type="image/png"/>
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
            <strong>Login</strong>
        </section>
        <section id="pageContent">
            <div class="card rounded">
                <form action="../cgi-bin/VerifyUser.py" method="POST">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email"><br>
                    <label for="password">Password</label> 
                    <input type="password" id="password" name="password"><br>
                    <input type="submit">
                </form>
            </div>
        </section>
        <footer>
            <p>&copy; 2020 by Hen Events | 3607 Trousdale Pkwy Los Angeles, CA 90089 | info@henevents.com</p>
        </footer>
    </body>
'''
checkout_script_1 = '''
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Checkout</title>
        <meta name="description" content="Hen Events checkout">
        <link rel="stylesheet" href="/WebContent/styles/style.css" />
        <script src="/WebContent/scripts/script.js"></script>
        <link rel="shortcut icon" href="/WebContent/images/flower-logo.png" type="image/png"/>
        <link rel="icon" href="/WebContent/images/flower-logo.png" type="image/png"/>
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
            <strong>Checkout</strong>
        </section>
        <section id="pageContent">
            <div class="card rounded">'''

checkout_script_2 = '''
                <p>Selected Bundle: <b>{0}</b></p><br>
                <p>Price: <b>${1}</b></p><br>
                <form action="../cgi-bin/AddOrder.py" method="POST">
                    <label for="fname">First Name</label><br>
                    <input type="text" id="fname" name="fname" value="{2}"><br><br>
                    <label for="lname">Last Name</label><br>
                    <input type="text" id="lname" name="lname" value="{3}"><br><br>
                    <label for="date">Event Date</label><br>
                    <input type="date" id="date"  name="date"><br><br>
                    <label for="time">Event Time</label><br>
                    <input type="time" id="time" name="time"><br><br>
                    <label for="ename">Event Name</label><br>
                    <input type="text" id="ename" name="ename"><br><br>
                    <label for="desc">Event Details</label><br>
                    <textarea rows="4" cols="60" name="desc"></textarea><br><br>
                    <input type="submit" value="Continue to Purchase Method">
                    <input type="hidden" name="user_id" value="{4}">
                    <input type="hidden" name="prod_id" value="{5}">
                </form>
            </div>
        </section>
        <footer>
            <p>&copy; 2020 by Hen Events | 3607 Trousdale Pkwy Los Angeles, CA 90089 | info@henevents.com</p>
        </footer>
    </body>'''

def isLoggedIn(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM loggedin_user")
    row = cursor.fetchone()
    if row is not None:
        return row[1]
    else:
        return -1
    cursor.close()

error = False
try:
    conn = mysql.connector.connect(host='localhost',
                                   user='root',
                                   password='password')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS hen")
        cursor.execute("USE hen")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS loggedin_user (
                zero INT(1) PRIMARY KEY,
                id INT(6),
                CONSTRAINT fk_id FOREIGN KEY (id) REFERENCES users(user_id)
            )
        ''')
        try:
            try:
                user_id = isLoggedIn(conn)
                if user_id == -1:
                    print(login_script)
                else:
                    print(checkout_script_1)
                    cursor.execute("SELECT * FROM users WHERE user_id={0}".format(user_id))
                    row = cursor.fetchone()
                    print(checkout_script_2.format(input_data["product"].value, input_data["price"].value, row[1], row[2], user_id, input_data["prod_id"].value))
            except KeyError as ke:
                print("<p>Form values cannot be blank!</p>")
                error = True
            except Error as e:
                print("<p>", e, "</p>")
            finally:
                cursor.close()
        except Error as e:
                track = traceback.format_exc()
                print("<p>{0}</p>".format(track))
                error = True
    else:
        print('<p>Unable to connect to MySQL database</p>')
        error = True
except Error as e:
    print('<p>',traceback.format_exc(),'</p>')
    error = True
finally:
    if conn is not None and conn.is_connected():
        conn.close()
