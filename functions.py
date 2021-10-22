import random

def c(session):
  return "username" in session

def u(session):
  return session["username"]