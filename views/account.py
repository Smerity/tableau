import sys
sys.path.append("..")


import db.database
import errno
import hashlib
import template.template
import mimetypes
import os
import re
from views.helper import get_logged_in

def logout(response):
    response.clear_cookie('userid')
    response.redirect('/')

def hash_password(passwd):
    # Note: this isn't really secure but it's better than plaintext
    # Use a proper solution such as scrypt/bcrypt/etc and read about salting
    s = passwd.encode('utf-8')
    return hashlib.sha256(s).hexdigest()

def login(response):
    username = response.get_field("username")
    password = response.get_field("password")
    current_user = get_logged_in(response)
    user = db.database.get_user(username)
    if user:
        if hash_password(password) == user.password:
            response.set_secure_cookie('userid', username)
            response.redirect('/')
        else:
            page_html = template.template.render("loginerror.html",
                                                 {'current_user':current_user,
                                                 "errors": ["Username or password incorrect"]})
            response.write(page_html)
    else:
        page_html = template.template.render("loginerror.html",
                                             {'current_user':current_user,
                                              "errors": ["Username or password incorrect"]})
        response.write(page_html)


def signup(response):
    errors = []
    username = response.get_field("username")
    password = response.get_field("password")
    password2 = response.get_field("password2")
    fname = response.get_field("fname")
    lname = response.get_field("lname")
    email = response.get_field("email")
    bday = response.get_field("bday")
    bmonth = response.get_field("bmonth")
    byear = response.get_field("byear")

    filename, content_type, data = response.get_file("profilepic")

    # check for logged in user
    current_user = get_logged_in(response)

    if current_user:
        errors.append("You already have an account.")
        page_html = template.template.render("signup.html",{'show_chat': False, 'current_user':current_user, "errors":errors})
        response.write(page_html)
        return
    if not username:
        page_html = template.template.render("signup.html",{'show_chat': False, 'current_user':current_user, "errors":errors})
        response.write(page_html)
        return

    is_valid = True

    if db.database.get_user(username):
        is_valid = False
        errors.append("This user already exists")

    if not re.match(r'^[A-Za-z0-9\._]+$', username):
        is_valid = False
        errors.append("Your username consisted of illegal characters")
    if len(username) < 2:
        is_valid = False
        errors.append("Your username must be greater than 2 characters")
    if len(password) < 6:
        is_valid = False
        errors.append("Your password must be greater than or equal to six characters")
    if username == password:
        is_valid = False
        errors.append("Your username and password cannot match")
    if password != password2:
        is_valid = False
        errors.append("Your passwords do not match")
    if not fname:
        is_valid = False
        errors.append("You did not enter a first name")
    if not lname:
        is_valid = False
        errors.append("You did not enter a last name")
    if not email:
        is_valid = False
        errors.append("You did not enter an email")
    if not (bday and bmonth and byear):
        is_valid = False
        errors.append("You must have birth date month and year")


    if is_valid:
        # ensure the profile directory exists
        try:
            os.makedirs(os.path.join('static', 'images', 'profile'))
        except OSError as e:
            # makedirs raises an error if it already exists, ignore that error
            # but re-raise any others.
            if e.errno != errno.EEXIST:
                raise
        if filename:
            extension = mimetypes.guess_extension(content_type)
            filename = username + extension
            image_id = (filename, content_type, data)
            if image_id:
                    photo_path = os.path.join('static', 'images', 'profile', filename)
                    with open(photo_path, 'wb') as f:
                        f.write(data)
        else:
            extension = None

        user = db.database.create_user(username, hash_password(password), fname, lname, bday, bmonth, byear, email, extension)
        response.set_secure_cookie('userid', username)
        response.redirect('/user/' + username)
    else:
        page_html = template.template.render("signup.html",{'show_chat': False, 'current_user':current_user, "errors":errors})
        response.write(page_html)

def edit_user(response, username):
    current_user = get_logged_in(response)
    if current_user == None or current_user.username != username:
        response.redirect("/")
        return
    fname = response.get_field("fname")
    lname = response.get_field("lname")
    email = response.get_field("email")
    bday = response.get_field("bday")
    bmonth = response.get_field("bmonth")
    byear = response.get_field("byear")
    filename, content_type, data = response.get_file("profilepic")
    print(filename)
    if filename:
            extension = mimetypes.guess_extension(content_type)
            filename = username + extension
            image_id = (filename, content_type, data)
            if image_id:
                    photo_path = os.path.join('static', 'images', 'profile', filename)
                    with open(photo_path, 'wb') as f:
                        f.write(data)

    if fname and email:
        user = db.database.get_user(username)
        if filename:
            db.database.update_user(user, fname=fname, lname=lname, bday=bday, bmonth=bmonth, byear=byear, email=email, filename=filename)
        else:
            db.database.update_user(user, fname=fname, lname=lname, bday=bday, bmonth=bmonth, byear=byear, email=email)
        response.set_secure_cookie('userid', username)
        response.redirect('/user/' + username)
    else:
        page_html = template.template.render("edit_user.html",{'current_user':current_user})
        response.write(page_html)

def change_password(response, username):
    # check for logged in user
    current_user = get_logged_in(response)
    if current_user == None or current_user.username != username:
        response.redirect("/")
        return
    username = current_user.username
    password = current_user.password
    #loads password in database for comparison
    user = db.database.get_user(username)
    password = user.password

    #loads form data from change_password.html
    old_password = response.get_field("old_password")
    new_password = response.get_field("new_password")
    new_password1 = response.get_field("new_password1")

    #checks validity of data
    if hash_password(old_password) == password:
        if len(new_password) > 5 and username != new_password and new_password == new_password1:
            db.database.update_user(user, password=hash_password(new_password))
            response.set_secure_cookie('userid', username)
            response.redirect('/user/' + username)
    else:
        page_html = template.template.render("change_password.html",{'current_user':current_user})
        response.write(page_html)
