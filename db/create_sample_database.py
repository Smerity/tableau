import sqlite3

# SQL Statements

CREATE_USERS_TABLE = '''
CREATE TABLE users (
    id INTEGER NOT NULL,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    bday INTEGER,
    bmonth INTEGER,
    byear INTEGER,
    email TEXT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,

    PRIMARY KEY (id),
    UNIQUE (username)
);
'''

CREATE_IMAGES_TABLE = '''
CREATE TABLE images (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    data BLOB NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
'''

CREATE_EDITORS_TABLE = '''
CREATE TABLE editors (
    user_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
    FOREIGN KEY (image_id) REFERENCES images (id)
);
'''

CREATE_FRIENDS_TABLE = '''
CREATE TABLE friends (
    user_id INTEGER NOT NULL,
    friend_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
    FOREIGN KEY (friend_id) REFERENCES users(id)
);
'''

#def insert_user(username, password, name):
 # conn = cur = None
try:
  conn = sqlite3.connect('Tableau.db')
  cur = conn.cursor()
  cur.execute(CREATE_USERS_TABLE)
  cur.execute(CREATE_IMAGES_TABLE)
  cur.execute(CREATE_EDITORS_TABLE)
  cur.execute(CREATE_FRIENDS_TABLE)
  #print(cur.execute('SELECT * FROM users;').fetchall())

  cur.execute('''INSERT INTO users VALUES (NULL, ? ,? , ?, ?, ?, ?, ?, ?);''',('Stephen', 'Merity', 28, 8, 1981, 'SmerityLikesPie@hotmail.com', 'smerity', 'password')) 

  
finally:
  if cur:
    cur.close()
  if conn:
    conn.close()