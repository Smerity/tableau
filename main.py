from tornado.ncss import Server
import re
import template.template
import db.database
import mimetypes
import os
import smtplib

from views.helper import get_logged_in

from views.account import change_password, login, logout, signup, edit_user
from views.user import redirect_user, user
from views.image import gallery, image_upload, image, create_comment, delete_image
from views.chat import ChatWebSocket
from views.canvas import CanvasWebSocket

if not os.path.exists("Tableau.db"):
    db.database.create_database()
    db.database.create_user('testuser', 'password', 'test', 'user', 31, 1, 1000, 'gmail')

def index(response):
    current_user = get_logged_in(response)
    page_html = template.template.render("index.html", {'show_chat': False, 'current_user':current_user})
    response.write(page_html)
    
def helpme(response):
    current_user = get_logged_in(response)
    page_html = template.template.render("help.html", {'show_chat': False, 'current_user':current_user})
    response.write(page_html)

def about(response):
    current_user = get_logged_in(response)
    page_html = template.template.render("about.html", {'show_chat': False, 'current_user':current_user})
    response.write(page_html)

def help(response):
    current_user = get_logged_in(response)
    page_html = template.template.render("help.html", {'current_user':current_user})
    response.write(page_html)
    
def forgot_password_page(response):
    current_user = get_logged_in(response)
    page_html = template.template.render("forgot.html", {'show_chat': False, 'current_user':current_user})
    response.write(page_html)

def canvas(response):
    current_user = get_logged_in(response)
    page_html = template.template.render("canvas.html", {'show_chat': True, 'current_user':current_user})
    response.write(page_html)

server = Server(port = 8888)
server.register("/", index)
server.register("/signup/?", signup)
server.register("/logout/?", logout)
server.register("/login/?", login)
server.register("/user/([A-Za-z0-9\._]+)/edit/?", edit_user)
server.register("/user/([A-Za-z0-9\._]+)/change_password", change_password)
server.register("/help/?", helpme)
server.register("/gallery/?", gallery)
server.register("/image/?", image_upload)
server.register("/user/?", redirect_user)
server.register("/forgot/?", forgot_password_page)
server.register("/user/([A-Za-z0-9\._]+/?)", user)
server.register("/about/?", about)
server.register("/canvas/?", canvas)
server.register("/image/([0-9]+/?)", image)
server.register("/gallery/([0-9]+/?)", image)
server.register("/gallery/([0-9]+)/comment/?", create_comment)
server.register("/gallery/([0-9]+)/delete/?", delete_image)
server.register("/websocket/([a-zA-Z0-9-]+)", ChatWebSocket)
server.register("/savecanvas/([a-zA-Z0-9-]+)", CanvasWebSocket)

server.run()
