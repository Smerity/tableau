import sys
sys.path.append("..")


from tornado.websocket import WebSocketHandler
from views.helper import get_logged_in
import db.database
import base64
import os


class CanvasWebSocket(WebSocketHandler):
    def open(self, title):
        self.title = title.decode("utf-8")
        self.user = db.database.get_user(self.get_secure_cookie('userid').decode())
        print("Starting image with title {}".format(self.title))
    def on_message(self, message):
        print("image data (hopefully) received {}".format(self.title))
        header, data = message.split(',')
        self.image_id = db.database.create_image(self.user.username, self.title, ".png")
        image = db.database.get_image(self.image_id)
        photo_path = os.path.join('static', 'images', image.filename)
        data = base64.b64decode(data)
        with open(photo_path, 'wb') as f:
            f.write(data)
        
    def on_close(self):
      pass