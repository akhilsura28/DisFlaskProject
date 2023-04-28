import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, usermail,userpassword) VALUES (?, ?,?)",
            ('Shravan', 'svrn@gmail.com','Shravan@321')
            )

cur.execute("INSERT INTO users (username, usermail,userpassword) VALUES (?, ?,?)",
            ('Sharan', 'shrn@gmail.com','Sharan@987')
            )

connection.commit()
connection.close()