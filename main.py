import os, random, time
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from functions import *
from room import Room
from player import Player

app = Flask("app", static_url_path="")
app.config["SECRET_KEY"] = os.getenv("secret")

socketio = SocketIO(app)
rooms = {}
users = {}

@app.route("/")
def index():
  return render_template("index.html", loggedin=c(session), session=session)

@app.route("/", methods=["POST"])
def setusername():
  if "username" in request.form:
    if not request.form["username"].replace(" ", ""):
      return render_template("index.html", loggedin=c(session), session=session, error=True)
    session["username"] = request.form["username"]
    if "hosted" not in session:
      session["hosted"] = ""
    print(session)
  return redirect("/")

@app.route("/logout")
def logout():
  session.clear()
  return redirect("/")

@app.route("/join")
def join():
  if not c(session): return redirect("/")
  return render_template("join.html")

@app.route("/join", methods=["POST"])
def joinroom():
  if not c(session): return redirect("/")
  if "room" in request.form and request.form["room"] in rooms:
    return redirect("/game/" + request.form["room"])
  return render_template("join.html", error=True)

@app.route("/create")
def create():
  if not c(session): return redirect("/")
  return render_template("create.html")

@app.route("/create", methods=["POST"])
def createroom():
  if not c(session): return redirect("/")
  d = request.form
  host = session["username"]
  name = d["name"].replace(" ", "")
  privacy = d["privacy"]
  size = d["size"]
  maxplayers = d["maxplayers"]
  minnum = d["minnum"]
  maxnum = d["maxnum"]
  if not name:
    return render_template("create.html", error="Please enter a room name.")
  if name in rooms:
    return render_template("create.html", error="This room name is taken.")
  rooms[name] = Room(host, name, privacy, size, maxplayers, minnum, maxnum)
  print(rooms)
  if session["hosted"] == "":
    session["hosted"] += name 
  else:
    session["hosted"] += " " + name
  print(session)
  return redirect("/game/" + name)

@app.route("/game/<room>")
def game(room):
  if not c(session): return redirect("/")
  if room not in rooms:return "not a room"
  hostedrooms = session["hosted"]
  hosted = room
  gamehost = None
  if hostedrooms != room:
    hosted = hostedrooms.split(" ")
  host = (room in hosted)
  if rooms[room].host_joined:
    host = False
  if not host:
    gamehost = rooms[room].host
  return render_template("game.html", name=u(session), room=room, host=host, gamehost=gamehost)

"""
@app.route(os.getenv("url"))
def url():
  quit()
"""

@socketio.on("joined")
def joined(name, room):
  rooms[room].involved.append({request.sid:name})
  host = True
  if name == rooms[room].host and not rooms[room].host_joined:
    rooms[room].host_joined = True
  else:
    player = Player(name, request.sid, room)
    player.generate_board(rooms)
    rooms[room].players.append(player)
    host = False  
  print(rooms[room].__dict__)
  join_room(room)
  if not host:
    emit("gameboard", player.board, room=request.sid)

@socketio.on("disconnect")
def disconnect():
  pass

socketio.run(app, host="0.0.0.0", port=8080)