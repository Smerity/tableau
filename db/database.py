'''
This module contains functions for reading and writing and deleting from the
database. Change FILENAME to change the name of the database.
'''



import sqlite3
import os
import datetime

FILENAME = 'Tableau.db'



# SQL Statements

CREATE_USERS_TABLE = '''
CREATE TABLE users (
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    fname TEXT NOT NULL,
    lname TEXT,
    bday INTEGER,
    bmonth INTEGER,
    byear INTEGER,
    email TEXT NOT NULL,
    filename TEXT,
    
    PRIMARY KEY (username)
);
'''

CREATE_IMAGES_TABLE = '''
CREATE TABLE images (
    id INTEGER NOT NULL,
    username TEXT NOT NULL,
    title TEXT NOT NULL,
    extension TEXT NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES users (username)
);
'''

CREATE_EDITORS_TABLE = '''
CREATE TABLE editors (
    username TEXT NOT NULL,
    image_id INTEGER NOT NULL,
    
    FOREIGN KEY (username) REFERENCES users (username)
    FOREIGN KEY (image_id) REFERENCES images (id)
);
'''

CREATE_FRIENDS_TABLE = '''
CREATE TABLE friends (
    username TEXT NOT NULL,
    friend INTEGER NOT NULL,
    
    FOREIGN KEY (username) REFERENCES users (username)
    FOREIGN KEY (friend) REFERENCES users(username)
);
'''

CREATE_COMMENTS_TABLE = '''
CREATE TABLE comments (
    id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    text TEXT NOT NULL,
    second INTEGER NOT NULL,
    minute INTEGER NOT NULL,
    hour INTEGER NOT NULL,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,

    PRIMARY KEY (id)
    FOREIGN KEY (image_id) REFERENCES images (id)
    FOREIGN KEY (username) REFERENCES users (username)
);
'''



GET_MAX_IMAGE_ID = '''
SELECT MAX(id)
FROM images;
'''



CREATE_USER = '''
INSERT INTO users (username, password, fname, lname, bday, bmonth, byear, email, filename)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
'''

DELETE_USER = '''
DELETE FROM users
WHERE username = ?;
'''

DELETE_USER_IMAGES = '''
DELETE FROM images
WHERE username = ?;
'''

DELETE_USER_FRIENDS = '''
DELETE FROM friends
WHERE username = ?;
'''

GET_USER = '''
SELECT username, password, fname, lname, bday, bmonth, byear, email, filename
FROM users
WHERE username = ?;
'''

GET_USER_IMAGES = '''
SELECT image_id
FROM editors
WHERE username = ?;
'''

GET_USER_FRIENDS = '''
SELECT friend
FROM friends
WHERE username = ?;
'''

GET_USER_COMMENTS = '''
SELECT id
FROM comments
WHERE username = ?;
'''

UPDATE_USER = '''
UPDATE users
SET password = ?,
    fname = ?,
    lname = ?,
    bday = ?,
    bmonth = ?,
    byear = ?,
    email = ?,
    filename = ?
WHERE username = ?;
'''

CHECK_USER = '''
SELECT COUNT(username)
FROM users
WHERE username = ?;
'''

CREATE_IMAGE = '''
INSERT INTO images (username, title, extension)
VALUES (?, ?, ?);
'''

DELETE_IMAGE = '''
DELETE FROM images
WHERE id = ?;
'''

DELETE_IMAGE_EDITORS = '''
DELETE FROM editors
WHERE image_id = ?;
'''

DELETE_IMAGE_COMMENTS = '''
DELETE FROM comments
WHERE image_id = ?;
'''

GET_IMAGE = '''
SELECT id, username, title, extension
FROM images
WHERE id = ?;
'''

GET_IMAGES = '''
SELECT id
FROM images;
'''

GET_IMAGE_EDITORS = '''
SELECT username
FROM images
WHERE image_id = ?;
'''

GET_IMAGE_COMMENTS = '''
SELECT id
FROM comments
WHERE image_id = ?;
'''

CREATE_EDITOR = '''
INSERT INTO editors (username, image_id)
VALUES (?, ?);
'''

DELETE_EDITOR = '''
DELETE FROM editors
WHERE username = ? AND friend = ?;
'''

CREATE_FRIEND = '''
INSERT INTO friends (username, friend)
VALUES (?, ?);
'''

DELETE_FRIEND = '''
DELETE FROM friends
WHERE username = ? AND friend = ?;
'''

CREATE_COMMENT = '''
INSERT INTO comments (image_id, username, text, second, minute, hour, day, month, year)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
'''

DELETE_COMMENT = '''
DELETE FROM comments
WHERE id = ?;
'''

GET_COMMENT = '''
SELECT image_id, username, text, second, minute, hour, day, month, year
FROM comments
WHERE id = ?;
'''

UPDATE_COMMENT = '''
UPDATE comments
SET text = ?
WHERE id = ?;
'''



# Classes

class User:

    def __init__(self, username, password, fname, lname, bday, bmonth, byear, email, filename):
        self.username = username
        self.password = password
        self.fname = fname
        self.lname = lname
        self.bday = bday
        self.bmonth = bmonth
        self.byear = byear
        self.email = email
        self.filename = filename

    def __str__(self):
        return 'Username: {}\nPassword: {}\nName: {} {}\nBirth Date: {}/{}/{}\nEmail: {}\nFilename: {}'.format(self.username,
                                                                                                               self.password,
                                                                                                               self.fname,
                                                                                                               self.lname,
                                                                                                               self.bmonth,
                                                                                                               self.bday,
                                                                                                               self.byear,
                                                                                                               self.email,
                                                                                                               self.filename)

    def get_data(self):
        return [self.username,
                self.password,
                self.fname,
                self.lname,
                self.bday,
                self.bmonth,
                self.byear,
                self.email,
                self.filename]

class Image:

    def __init__(self, image_id, username, title, extension):
        self.id = image_id
        self.username = username
        self.title = title
        self.extension = extension
        self.filename = str(self.id)+self.extension

    def __str__(self):
        return 'ID: {}\nOwner: {}\nTitle: {}\nExtension: {}\nFilename: {}'.format(self.id,
                                                                                  self.username,
                                                                                  self.title,
                                                                                  self.extension,
                                                                                  self.filename)

    def get_data(self):
        return [self.id,
                self.username,
                self.title,
                self.extension,
                self.filename]

class Comment:

    def __init__(self, comment_id, image_id, username, text, second, minute, hour, day, month, year):
        self.id = comment_id
        self.image_id = image_id
        self.username = username
        self.text = text
        self.second = second
        self.minute = minute
        self.hour = hour
        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        return 'ID: {}\nImage ID: {}\nUsername: {}\nText: {}\nDatetime: {}-{}-{} {}:{}:{}'.format(self.id,
                                                                                                  self.image_id,
                                                                                                  self.username,
                                                                                                  self.text,
                                                                                                  self.year,
                                                                                                  self.month,
                                                                                                  self.day,
                                                                                                  self.hour,
                                                                                                  self.minute,
                                                                                                  self.second)

    def get_data(self):
        return [self.id,
                self.image_id,
                self.username,
                self.text,
                self.second,
                self.minute,
                self.hour,
                self.day,
                self.month,
                self.year]



# Functions

def create_database():
    '''
    Creates tables in the database.
    '''
    
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(CREATE_USERS_TABLE)
        cur.execute(CREATE_IMAGES_TABLE)
        cur.execute(CREATE_EDITORS_TABLE)
        cur.execute(CREATE_FRIENDS_TABLE)
        cur.execute(CREATE_COMMENTS_TABLE)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def delete_database():
    '''
    Deletes all tables in the database.
    '''
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute('DROP TABLE users;')
        cur.execute('DROP TABLE images;')
        cur.execute('DROP TABLE editors;')
        cur.execute('DROP TABLE friends;')
        cur.execute('DROP TABLE comments;')
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_database():
    '''
    Returns a dictionary. Keys are table names, and values are a list of
    records.
    '''
    
    data = None
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        data = {}
        data['users'] = cur.execute('SELECT * FROM users;').fetchall()
        data['images'] = cur.execute('SELECT * FROM images;').fetchall()
        data['editors'] = cur.execute('SELECT * FROM editors;').fetchall()
        data['friends'] = cur.execute('SELECT * FROM friends;').fetchall()
        data['comments'] = cur.execute('SELECT * FROM comments;').fetchall()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return data

def create_user(username, password, fname, lname, bday, bmonth, byear, email, extension=None):
    '''
    Creates a user.
    '''

    if not extension:
        filename = 'default.jpeg'
    else:
        filename = username+extension
    
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(CREATE_USER, (username, password, fname, lname, bday, bmonth, byear, email, filename))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def delete_user(username):
    '''
    Deletes a user.
    '''
    
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(DELETE_USER, (username,))
        conn.commit()
        delete_user_images(username)
        delete_user_friends(username)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def delete_user_images(username):
    '''
    Deletes all of the images owned by the user.
    '''

    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(DELETE_USER_IMAGES, (username,))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def delete_user_friends(username):
    '''
    Deletes all of the user's friends.
    '''
    
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(DELETE_USER_FRIENDS, (username,))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_user(username):
    '''
    Returns a User object if the user exists, otherwise returns None.
    '''
    
    user = None
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        user_data = cur.execute(GET_USER, (username,)).fetchone()
        user = User(*user_data)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return user

def get_user_images(username):
    '''
    Returns a list of the ids of all images created by the user.
    '''
    
    images = None
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        images = cur.execute(GET_USER_IMAGES, (username,)).fetchall()
        images = [image[0] for image in images]
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return images

def get_user_friends(username):
    '''
    Returns a list of the ids of all friends of the user.
    '''
    
    friends = None
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        friends = cur.execute(GET_USER_FRIENDS, (username,)).fetchall()
        friends = [friend[0] for friend in friends]
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return friends

def get_user_comments(username):
    '''
    Returns a list of the ids of all comments made by the user.
    '''
    
    comments = None
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        comments = cur.execute(GET_USER_COMMENTS, (username,)).fetchall()
        comments = [comment[0] for comment in comments]
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return comments

def update_user(user, **kwargs):
    '''
    Updates a user. You cannot update their username.
    '''
    
    for arg in kwargs:
        if arg == 'password':
            user.password = kwargs[arg]
        elif arg == 'fname':
            user.fname = kwargs[arg]
        elif arg == 'lname':
            user.lname = kwargs[arg]
        elif arg == 'bday':
            user.bday = kwargs[arg]
        elif arg == 'bmonth':
            user.bmonth = kwargs[arg]
        elif arg == 'byear':
            user.byear = kwargs[arg]
        elif arg == 'email':
            user.email = kwargs[arg]
        elif arg == 'filename':
            user.filename = kwargs[arg]
        else:
            raise TypeError('Argument does not exist.\n        - Caiden')

    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(UPDATE_USER, (user.password, user.fname, user.lname, user.bday, user.bmonth, user.byear, user.email, user.filename, user.username))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def check_user(username):
    '''
    Checks whether the user exists.
    '''

    exists = None
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        count = cur.execute(CHECK_USER, (username,))
        if count == 0:
            exists = False
        else:
            exists = True
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return exists
    
def create_image(username, title, extension):
    '''
    Creates an image.
    '''

    image_id = None
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(CREATE_IMAGE, (username, title, extension))
        conn.commit()
        image_id = cur.execute(GET_MAX_IMAGE_ID).fetchone()[0]
        create_editor(username, image_id)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return image_id

def delete_image(image_id):
    '''
    Deletes an image.
    '''
    
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(DELETE_IMAGE, (image_id,))
        conn.commit()
        delete_image_editors(image_id)
        delete_image_comments(image_id)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def delete_image_editors(image_id):
    '''
    Deletes all links between the image and it's editors.
    '''

    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(DELETE_IMAGE_EDITORS, (image_id,))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def delete_image_comments(image_id):
    '''
    Deletes all comments made on the image.
    '''

    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(DELETE_IMAGE_COMMENTS, (image_id,))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_image(image_id):
    '''
    Returns an Image object.
    '''
    
    image = None
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        image_data = cur.execute(GET_IMAGE, (image_id,)).fetchone()
        image = Image(*image_data)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return image

def get_images():
    '''
    Returns a list of the ids of all the images.
    '''
    
    images = None
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        images = cur.execute(GET_IMAGES).fetchall()
        images = [image[0] for image in images]
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return images

def get_image_editors(image_id):
    '''
    Returns a list of the ids of all the users who have participated in editing
    the image.
    '''
    
    editors = None
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        editors = cur.execute(GET_IMAGE_EDITORS, (image_id,)).fetchall()
        editors = [editor[0] for editor in editors]
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return editors

def get_image_comments(image_id):
    '''
    Returns a list of the ids of all the comments that have been made on the
    image.
    '''
    
    comments = None
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        comments = cur.execute(GET_IMAGE_COMMENTS, (image_id,)).fetchall()
        comments = [comment[0] for comment in comments]
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return comments

def create_editor(username, image_id):
    '''
    Creates a link between a user and an image.
    '''
    
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(CREATE_EDITOR, (username, image_id))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def delete_editor(username, image_id):
    '''
    Deletes a link between a user and an image.
    '''
    
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(DELETE_EDITOR, (username, image_id))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def create_friend(username, friend):
    '''
    Adds a friend to a user.
    '''
    
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(CREATE_FRIEND, (username, friend))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def delete_friend(username, friend):
    '''
    Deletes a friend from a user.
    '''
    
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(DELETE_FRIEND, (username, friend))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def create_comment(image_id, username, text):
    '''
    Adds a comment to an image by a particular user.
    '''
    
    dt = datetime.datetime.now()
    second = dt.second
    minute = dt.minute
    hour = dt.hour
    day = dt.day
    month = dt.month
    year = dt.year
    
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(CREATE_COMMENT, (image_id, username, text, second, minute, hour, day, month, year))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def delete_comment(comment_id):
    '''
    Deletes a comment from an image.
    '''
    
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(DELETE_COMMENT, (comment_id,))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_comment(comment_id):
    '''
    Returns a Comment object.
    '''
    
    comment = None
    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        comment_data = cur.execute(GET_COMMENT, (comment_id,)).fetchone()
        comment = Comment(comment_id, *comment_data)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return comment

def update_comment(comment, **kwargs):
    '''
    Updates a comment.
    '''
    
    for arg in kwargs:
        if arg == 'text':
            comment.text = kwargs[arg]
        else:
            raise TypeError('Argument does not exist.\n        - Caiden')

    conn = cur = None
    try:
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute(UPDATE_COMMENT, (comment.text, comment.id))
        conn.commit()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



# Testing

if __name__ == '__main__':
    delete_database()
    create_database()
    create_user('caidenm', 'password', 'caiden', 'morjanoff', 31, 2, 3000, 'gmail')
    create_user('caidenm2', '123456', 'caiden2', 'morjanoff2', 31, 2, 4000, 'email')
    create_friend('caidenm', 'caidenm2')
    create_image('caidenm', 'test2', '.png')
    create_image('caidenm', 'something', '.jpeg')
    create_image('caidenm', 'anything', '.bmp')

    print(get_user('caidenm'))
    print(get_user('caidenm2'))
    print(get_user_images('caidenm'))
    print(get_user_friends('caidenm'))
    print(get_image(1))
    print(get_image(2))

    delete_friend('caidenm', 'caidenm2')
    
    print(get_user_friends('caidenm'))



# Create database if not present. Adds default user.

if not os.path.exists(FILENAME):
    create_database()
    create_user('testuser', 'password', 'test', 'user', 31, 1, 1000, 'gmail')
    create_user('admin', 'admin', 'Mr.', 'Admin', 10, 10, 10, 'gmail')
    create_friend('testuser', 'admin')
    create_friend('admin', 'testuser')
