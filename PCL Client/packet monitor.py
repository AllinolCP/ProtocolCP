import sys
import msvcrt
import hashlib
import os
import json
import client
import login

def get_room_id(name):
	filename = os.path.join(os.path.dirname(__file__), "json/rooms.json")
	with open(filename) as file:
		data = json.load(file)
	for id in data:
		if data[id] == name:
			return int(id)
	return 0

def get_room_name(id):
	filename = os.path.join(os.path.dirname(__file__), "json/rooms.json")
	with open(filename) as file:
		data = json.load(file)
	if str(id) in data:
		return data[str(id)]
	return "Unknown"

def room(client, params):
	if params:
		try:
			id = int(params[0])
		except ValueError:
			id = get_room_id(params[0])
			if not id:
				print "Room not found"
				return
		client.join_room(id)
	else:
		print "Current room: " + get_room_name(client.room_id)

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
	commands = {
		"room": room,
	}
	while True:
		print ">>>",
		cmd = raw_input().split(' ')
		name = cmd[0]
		params = cmd[1:]
		if name in commands:
			commands[name](client, params)
		else:
			print "command '" + name + "' doesn't exist"
