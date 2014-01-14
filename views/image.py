import sys
sys.path.append("..")


import db.database
import os
import mimetypes
import template.template
from views.helper import get_logged_in


def gallery(response):
    current_user = get_logged_in(response)
    if current_user:
        images = {}
        if current_user:
            for image_id in db.database.get_images():
                image = db.database.get_image(image_id)
                images[image.id] = image.filename

            page_html = template.template.render('gallery.html', {'show_chat': False, 'current_user':current_user, 'images': images})
            response.write(page_html)
    else:
        page_html = template.template.render("errorpage.html",
                                             {'current_user':current_user,
                                             "errors": ["Log in to view gallery"]})
        response.write(page_html)

ALLOWED_IMG_TYPES = set(['.jpg', '.png', '.gif', '.jpe', '.jpeg', '.bmp', '.tiff', '.exif'])
def image_upload(response):
    current_user = get_logged_in(response)
    if current_user is None:
        page_html = template.template.render("loginerror.html",
                                             {'current_user':current_user,
                                              "errors": ["Not currently logged in"]})
        response.write(page_html)
    elif response.request.method == "POST":
        filename, content_type,data = response.get_file('photo')
        if filename is None:
            page_html = template.template.render("file_upload.html",
                                                 {'current_user':current_user,
                                                  "errors": ["Empty filename"]})
            response.write(page_html)
        else:
            extension = mimetypes.guess_extension(content_type)
            if not extension or extension.lower() not in ALLOWED_IMG_TYPES:
               page_html = template.template.render("file_upload.html", {'current_user':current_user, 'user': current_user, 'errors': ['You can only upload images']})
               response.write(page_html)
            else:
                image_id = db.database.create_image(current_user.username, filename, extension)
                if image_id:
                    image = db.database.get_image(image_id)
                    photo_path = os.path.join('static', 'images', image.filename)
                    with open(photo_path, 'wb') as f:
                        f.write(data)
                    photo_url = '/gallery/'+ str(image_id)
                    response.redirect(photo_url)
                else:
                    page_html = template.template.render("loginerror.html",
                                                         {'current_user':current_user,
                                                          "errors": ["Image id not found in database"]})
                    response.write(page_html)
    else:
        page_html = template.template.render("file_upload.html",{'show_chat': False, 'current_user': current_user, 'user': current_user})
        response.write(page_html)


def get_image(image_id):
    image_to_view = db.database.get_image(image_id)
    if image_to_view:
        return image_to_view
    else:
        return None

def delete_image(response, image_id):
    current_user = get_logged_in(response)
    username = current_user.username
    if current_user == None or current_user.username != username:
        response.redirect("/gallery")
        return
    image_to_view = db.database.get_image(image_id)
    image_owner = image_to_view.username
    print (username)
    print (image_owner)
    if username == image_owner:
        db.database.delete_image(image_id)
    response.redirect("/gallery")
    return

def image(response, image_id):
    current_user = get_logged_in(response)
    if current_user:
        image_to_view = get_image(image_id)
        comments = get_comment_by_id(image_id)
        
        if image_to_view:
            print(comments)
            page_html = template.template.render("image.html",{'show_chat': True, 'get_user':db.database.get_user, 'current_user' : current_user, 'image': image_to_view, 'comment_list': comments})
            response.write(page_html)
        else:
            page_html = template.template.render("loginerror.html",
                                                 {'current_user':current_user,
                                                  "errors": ["Image does not exist"]})
            response.write(page_html)
    else:
        page_html = template.template.render("loginerror.html",
                                             {'current_user':current_user,
                                              "errors": ["You're not logged in"]})
        response.write(page_html)


#Comments

def create_comment(response, image_id):
    current_user = get_logged_in(response)
    if current_user:
        comment = response.get_field("comment")
        if comment:
            #try:
            db.database.create_comment(image_id, current_user.username, comment)
            response.redirect('../../../gallery/' + image_id)
            #except:
        else:
            page_html = template.template.render("loginerror.html",
                                                 {'current_user':current_user,
                                                  "errors": ["Image does not exist"]})
            response.write(page_html)
    else:
        page_html = template.template.render("loginerror.html",
                                             {'current_user':current_user,
                                              "errors": ["You're not logged in"]})
        response.write(page_html)

def get_comment_by_id(image_id):
    comment_list = []
    for comment_id in db.database.get_image_comments(image_id):
        print (comment_id)
        comment_individual = db.database.get_comment(int(comment_id))
        
        comment_list.append(comment_individual)
    return comment_list
#End comments
