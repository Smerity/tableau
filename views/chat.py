import sys
sys.path.append("..")


from tornado.websocket import WebSocketHandler
from views.helper import get_logged_in
import db.database

class ChatWebSocket(WebSocketHandler):
    open_connection = {}
    
   
    def open(self, page):
      self.page = page
      self.user = db.database.get_user(self.get_secure_cookie('userid').decode())
      if page not in ChatWebSocket.open_connection:
        ChatWebSocket.open_connection[page] = {'connections': [self], 'history': []}
      else:
        ChatWebSocket.open_connection[page]['connections'].append(self)
      for item in ChatWebSocket.open_connection[page]['history']:
        self.write_message(item)
      print(str(len(ChatWebSocket.open_connection)) + ' Users Online')
      
    def on_message(self, message): 
      ChatWebSocket.open_connection[self.page]['history'].append(self.user.username + ': ' + message)
      for open_connection in ChatWebSocket.open_connection[self.page]['connections']:
        if open_connection != self: 
            open_connection.write_message(self.user.username + ': ' + message)
      
    def on_close(self):
      ChatWebSocket.open_connection[self.page]['connections'].remove(self)
      if len(ChatWebSocket.open_connection[self.page]['connections']) == 0:
        del ChatWebSocket.open_connection[self.page]
      print(str(len(ChatWebSocket.open_connection)) + ' Users Online')
      print('A user has left the chatroom')