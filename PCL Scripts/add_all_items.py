import sys
import msvcrt
import hashlib
import os
import json
import client
import login
from time import sleep

if __name__ == "__main__":
	cpps = "PL"
	data = login.get_server(cpps)
	user = raw_input("Username: ").lower()
	password, encrypted = login.get_password(cpps, user)
	server = raw_input("Server: ").lower()
	
	ip = data["ip"]
	login_port = data["login"]
	game_port = data["servers"]
	if not server in game_port:
		sys.exit("Server not found")
	game_port = game_port[server]
	
	client = client.Client(ip, login_port, game_port, True)
	if not client.log:
		print "Connecting..."
	error = client.connect(user, password, encrypted)
	if error:
		sys.exit("Failed to connect")
	print "Connected!"
	client.join_room(811)
	client.add_coins(1600000)
	for i in xrange(1, 10000):
		client.add_item(i)
