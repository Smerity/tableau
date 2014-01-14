# db/helpers.py => get_user() return User or None
# class User: => first_name, last_name, username, email
import sqlite3 as lite
try:
    from . import database
except SystemError:
    import database
import os
users = {}




def get_user(username):
    '''this function allows you to get the user object for a particular USERNAME
        usage looks like...
        User = get_user("lochlanna")
        this returns an object from the database containing all of the info
        if the object does not exist "None" will be returned'''
    try:
        with open('Tableau.db'):
            con = lite.connect('Tableau.db')
            cursor = con.cursor()
            cursor.execute('''SELECT fname,lname,bday,bmonth,byear,email,username,password FROM users WHERE username=?''',(username,))
            row = cursor.fetchone()
            print(row)
            if row:
                U = User()
                U.fname = row[0]
                U.lname = row[1]
                U.bday = row[2]
                U.bmonth = row[3]
                U.byear = row[4]
                U.email = row[5]
                U.username = row[6]
                U.password = row[7]
            else:
                return None
    except IOError:
        U = users.get(username)
    return U
    
def create_user(fname,lname,bday,bmonth,byear,email,username,password):
    ''' this function allows you to create a NEW user object and also write the new data to the database
        usage of this function look like this
        create_user("lochlann","andrews",15,5,1997,"lochlanna@gmail.com","lochlanna","lochlannpword")'''
    U = User()
    U.fname = fname
    U.lname = lname
    U.bday = bday
    U.bmonth = bmonth
    U.byear = byear
    U.email = email
    U.username = username
    U.password = password
    users[username] = U
    try:
        with open('Tableau.db'):
            con = lite.connect('Tableau.db')
            cursor = con.cursor()
            cursor.execute('''INSERT INTO users VALUES (?,?,?,?,?,?,?,?)''',(username,password,fname,lname,bday,bmonth,byear,email))
            con.commit()
            print("user created")
    except IOError:
        print("file does not exist yet")
    return U



class User:
    def __init__(self):
        self.id = None
        self.fname = None
        self.lname = None
        self.bday = 0
        self.bmonth = 0
        self.byear = 0
        self.email = None
        self.username = None
        self.password = None
    def __repr__(self):
         return "[user, username:"+self.username +"]"

    def update_user(self,fname = None,lname = None,bday = None,bmonth = None,byear = None,email = None,password = None):
        ''' this function allows you to update data within the user object and also write the new data to the database
            usage of this function look like this
            user.update_user(password="newpassword",email = "looser@trololol.com.au")'''
        if fname is not None:
            self.fname = fname
        if lname is not None:
            self.lname = lname
        if bday is not None:
            self.bday = bday
        if bmonth is not None:
            self.bmonth = bmonth
        if byear is not None:
            self.byear = byear
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password
        try:
            with open('Tableau.db'):
                con = lite.connect('Tableau.db')
                cursor = con.cursor()
                cursor.execute('''UPDATE users SET fname=?,lname=?,bday=?,bmonth=?,byear=?,email=?,password=? WHERE username=?''',
                               (self.fname,self.lname,self.bday,self.bmonth,self.byear,self.email,self.password,self.username))
                con.commit()
        except IOError:
            users[self.username] = self
            print("file does not exist yet")

if not os.path.exists('Tableau.db'):
    database.create_database()
    create_user("Timothy","Dawborn",15,5,1997,"tim.dawborn@sydney.edu.au","timothy","timothydawborn")
         
if __name__ == "__main__":
    try:
        with open('Tableau.db'):
            con = lite.connect('Tableau.db')
            cursor = con.cursor()
            cursor.execute('''DELETE FROM users''')
            con.commit()
    except IOError:
        print("file does not exist yet")

    print("------------------------testing create user-----------------")
    create_user("lochlann","andrews",15,5,1997,"lochlanna@gmail.com","lochlanna","lochlannpword")
    print("------------------------should print a dict containing user-----------------")
    print(users)
    print("----------------------testing get user----------------------------")
    U = get_user("lochlanna")
    print("----------------------should print a user obj-----------------------")
    print(U)
    print("------------------------testing changing values-------------------")
    print("the old password was... "+U.password)
    U.update_user(password="hello world new password")
    print("the new password is... "+U.password)
    print("----------------------testing getting a user that does not exist----------------------")
    print("----------------------result should be 'None'----------------------")
    print(get_user("lochlanna1"))
    
    
