import sys
import db.database
sys.path.append("..")


import template.template
from views.helper import get_logged_in

def redirect_user(response):
    current_user = get_logged_in(response)
    if current_user:
        response.redirect('/user/' + current_user.username)
    else:
        response.redirect('/')

def user(response, username):
    user = get_logged_in(response)
    if username:
        profileuser = db.database.get_user(username)
        if not profileuser or not user:
            #if profile user is none
            response.redirect('/')
        else:
            #it is a real user so display their page
            page_html = template.template.render("user.html",{'show_chat': False, 'user':profileuser,'current_user':user,'viewed_username': username})
            response.write(page_html)
    else:
        #the username is either 'None' or '/'
        if user:
            page_html = template.template.render("user.html",{'show_chat': False, 'user':user,'current_user':user,'viewed_username': username})
            response.write(page_html)
        else:
            response.redirect('/')
