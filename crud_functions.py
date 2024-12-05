import sqlite3

def initiate_db():
    connection = sqlite3.connect('pr_db.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INT NOT NULL
    )
    ''')
    connection.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('pr_db.db')
    cursor = connection.cursor()

    cursor.execute("SELECT title, description, price FROM Products")
    return cursor.fetchall()


    connection.commit()
    connection.close()
    return users

def add_user(username, email, age):
    connection = sqlite3.connect('pr_db.db')
    cursor = connection.cursor()

    cursor.execute(f"INSERT INTO Users (username, email, age, balance) VALUES ('{username}', '{email}', '{age}', 1000)")
      
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('pr_db.db')
    cursor = connection.cursor()

    user_in = True
    check_user = cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if check_user.fetchone() is None:
         user_in = False

    return user_in


    connection.commit()
    connection.close()

initiate_db()
