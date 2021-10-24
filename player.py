from functions import random

class Player():
  def __init__(self, name, sid, room):
    self.name = name
    self.room = room
    self.sid = sid
    self.board = []
    
  def generate_board(self, rooms):
    info = rooms[self.room]
    for i in range(info.size):
      part = []
      for i in range(info.size):
        part.append({random.randint(info.minnum, info.maxnum):False})
      self.board.append(part)

  def check_for_connect(self):
    return False