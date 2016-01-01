import webapp2
import os

def fetchChallonge():
  path = os.path.join(os.path.dirname(__file__),"config.cfg")
  f = open(path)
  for line in f:
    parts = line.split(":")
    if len(parts) >= 2:
      if parts[1].endswith("\n"):
        parts[1] = parts[1][:-1]
    if parts[0] == "CHALLONGE_USERNAME":
      CHALLONGE_USERNAME = parts[1]
    elif parts[0] == "CHALLONGE_API":
      CHALLONGE_API = parts[1]
  return (CHALLONGE_USERNAME, CHALLONGE_API)

def fetchAdmin():
  path = os.path.join(os.path.dirname(__file__),"config.cfg")
  f = open(path)
  Admin = []
  for line in f:
    parts = line.split(":")
    if len(parts) >= 2:
      if parts[1].endswith("\n"):
        parts[1] = parts[1][:-1]
    if parts[0] == "ADMIN":
      Admin.append(parts[1])
  return Admin