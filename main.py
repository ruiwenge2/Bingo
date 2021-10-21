import os, random
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit

app = Flask("app", static_url_path="")
app.config["SECRET_KEY"] = os.getenv("secret")

socketio = SocketIO(app)
rooms = {}
users = {}

def check():
  return "username" in session

def username():
  return session["username"]

class Room():
  def __init__(self, host, name, privacy, size, maxplayers, minnum, maxnum):
    self.host = host
    self.name = name
    self.privacy = privacy
    self.size = size
    self.maxplayers = maxplayers
    self.minnum = minnum
    self.maxnum = maxnum
    self.players = []
    
  def generateNumber(self):
    return random.randint(self.minnum, self.maxnum)

class Player():
  def __init__(self, name, room):
    self.name = name
    self.room = room
    
  def generateBoard(self):
    pass

  def checkForConnect(self):
    return False

@app.route("/")
def index():
  return render_template("index.html", loggedin=check(), session=session)

@app.route("/", methods=["POST"])
def setusername():
  if "username" in request.form:
    if not request.form["username"].replace(" ", ""):
      return render_template("index.html", loggedin=check(), session=session, error=True)
    session["username"] = request.form["username"]
    if "hosted" not in session:
      session["hosted"] = []
    print(session)
  return redirect("/")

@app.route("/join")
def join():
  if not check(): return redirect("/")
  return render_template("join.html")

@app.route("/join", methods=["POST"])
def joinroom():
  if not check(): return redirect("/")
  if "room" in request.form and request.form["room"] in rooms:
    return redirect("/game/" + request.form["room"])
  return render_template("join.html", error=True)

@app.route("/create")
def create():
  if not check(): return redirect("/")
  return render_template("create.html")

@app.route("/create", methods=["POST"])
def createroom():
  if not check(): return redirect("/")
  d = request.form
  host = session["username"]
  name = d["name"]
  privacy = d["privacy"]
  size = d["size"]
  maxplayers = d["maxplayers"]
  minnum = d["minnum"]
  maxnum = d["maxnum"]
  if not name.replace(" ", ""):
    return render_template("create.html", error="Please enter a room name.")
  if name in rooms:
    return render_template("create.html", error="This room name is taken.")
  rooms[name] = Room(host, name, privacy, size, maxplayers, minnum, maxnum)
  print(rooms)
  session["hosted"].append(name)
  print(session)
  return redirect("/game/" + name)

@app.route("/game/<room>")
def game(room):
  if not check(): return redirect("/")
  if room not in rooms:return "not a room"
  host = (room in session["hosted"])
  # if rooms[room].host == username():
  #   host = False
  return render_template("game.html", host=host)

"""
@app.route(os.getenv("url"))
def url():
  quit()
"""

@socketio.on("joined")
def joined(name):
  pass

socketio.run(app, host="0.0.0.0", port=8080)