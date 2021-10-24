from functions import random

class Room():
  def __init__(self, host, name, privacy, size, maxplayers, minnum, maxnum):
    self.host = host
    self.name = name
    self.privacy = privacy
    self.size = int(size)
    self.maxplayers = maxplayers
    self.minnum = int(minnum)
    self.maxnum = int(maxnum)
    self.host_joined = False
    self.involved = []
    self.players = []
    
  def generate_number(self):
    return random.randint(self.minnum, self.maxnum)

  def check_for_bingo(self):
    pass