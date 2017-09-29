import socket
import hashlib
import re
import os
import json
import threading

class Penguin:
	def __init__(self, id, name, clothes, frame, x, y):
		self.id = id
		self.name = name
		self.clothes = clothes
		self.frame = frame
		self.x = x
		self.y = y
	
	@classmethod
	def from_player(cls, player):
		player = player.split('|')
		id = int(player[0])
		name = player[1]
		clothes = {}
		frame = player[2]
		types = ["color", "head", "face", "neck", "body", "hand", "feet", "pin", "background"]
		for i in range(len(types)):
			if player[i + 3]:
				clothes[types[i]] = int(player[i + 3])
		x = int(player[12])
		y = int(player[13])
		return cls(id, name, clothes, frame, x, y)

class Client:
	def __init__(self, login_ip, login_port, game_ip, game_port, magic=None, log=False):
		self.login_ip = login_ip
		self.login_port = login_port
		self.game_ip = game_ip
		self.game_port = game_port
		self.log = log
		self.magic = magic or "Y(02.>'H}t\":E1"
		self.buf = ""
		self.internal_room_id = -1
		self.id = -1
		self.coins = -1
		self.room_id = -1
		self.penguins = {}
		self.followed = None

	@staticmethod
	def swapped_md5(password, encrypted=False):
		if not encrypted:
			password = hashlib.md5(password).hexdigest()
		password = password[16:32] + password[0:16]
		return password

	def _send(self, data):
		if self.log:
			print "# SEND: " + str(data)
		try:
			self.sock.send(data + chr(0))
			return True
		except:
			print "Connection lost"
			return False

	def _send_packet(self, ext, cmd, *args):
		packet = "%xt%" + ext + "%" + cmd + "%"
		if args and args[0] is None:
			args = args[1:]
		else:
			args = (self.internal_room_id,) + args
		packet += "%".join(str(arg) for arg in args) + "%"
		return self._send(packet)

	def _receive(self):
		data = ""
		try:
			while not chr(0) in self.buf:
				data += self.buf
				self.buf = self.sock.recv(4096)
		except:
			return None
		i = self.buf.index(chr(0)) + 1
		data += self.buf[:i]
		self.buf = self.buf[i:]
		if self.log:
			print "# RECEIVE: " + str(data)
		return data

	def _receive_packet(self):
		data = self._receive()
		if not data:
			return None
		if data.startswith("%"):
			packet = data.split('%')
			if packet[2] == "e":
				self._error(packet)
			return packet
		raise Exception("Invalid packet")

	def _error(self, packet):
		filename = os.path.join(os.path.dirname(__file__), "json/errors.json")
		with open(filename) as file:
			data = json.load(file)
		code = int(packet[4])
		msg = "Error #" + str(code)
		if str(code) in data:
			msg += ": " + data[str(code)]
		if self.followed and self.followed["commands"]:
			self.say(msg)
		print msg

	def _ver_check(self, ver):
		if self.log:
			print "Sending 'verChk' request..."
		if not self._send('<msg t="sys"><body action="verChk" r="0"><ver v="' + str(ver) + '"/></body></msg>'):
		# if not self._send("<msg t='sys'><body action='verChk' r='0'><ver v='" + str(ver) + "' /></body></msg>"):
			return False
		data = self._receive()
		if not data:
			return False
		if "apiOK" in data:
			if self.log:
				print "Received 'apiOK' response"
			return True
		if "apiKO" in data:
			if self.log:
				print "Received 'apiKO' response"
			return False
		raise Exception("Invalid response")

	def _key(self):
		if self.log:
			print "Sending rndK request..."
		if not self._send('<msg t="sys"><body action="rndK" r="-1"></body></msg>'):
		# if not self._send("<msg t='sys'><body action='rndK' r='-1'></body></msg>"):
			return None
		data = self._receive()
		if not data:
			return None
		if 'rndK' in data:
			key = re.search("<k>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/k>", data).group(1)
			if self.log:
				print "Received key: " + key
			return key
		raise Exception("Invalid response")

	def _login(self, user, password, encrypted, ver):
		if self.log:
			print "Logging in..."
		if not self._ver_check(ver):
			return None, False
		rndk = self._key()
		if not rndk:
			return None, False
		hash = self.swapped_md5(self.swapped_md5(password, encrypted).upper() + rndk + self.magic)
		if not self._send('<msg t="sys"><body action="login" r="0"><login z="w1"><nick><![CDATA[' + user + ']]></nick><pword><![CDATA[' + hash + ']]></pword></login></body></msg>'):
		# if not self._send("<msg t='sys'><body action='login' r='0'><login z='w1'><nick><![CDATA[" + user + "]]></nick><pword><![CDATA[" + hash + "]]></pword></login></body></msg>"):
			return None, False
		packet = self._receive_packet()
		if not packet or packet[2] == "e":
			return packet, False
		while packet[2] != "l":
			packet = self._receive_packet()
			if not packet or packet[2] == "e":
				return packet, False
		if self.log:
			print "Logged in"
		return packet, True

	def _join_server(self, user, login_key, confirmation, ver):
		if self.log:
			print "Joining server..."
		if not self._ver_check(ver):
			return None, False
		rndk = self._key()
		if not rndk:
			return None, False
		hash = self.swapped_md5(login_key + rndk) + login_key
		if confirmation:
			hash += '#' + confirmation
		if not self._send('<msg t="sys"><body action="login" r="0"><login z="w1"><nick><![CDATA[' + user + ']]></nick><pword><![CDATA[' + hash + ']]></pword></login></body></msg>'):
		# if not self._send("<msg t='sys'><body action='login' r='0'><login z='w1'><nick><![CDATA[" + user + "]]></nick><pword><![CDATA[" + hash + "]]></pword></login></body></msg>"):
			return None, False
		packet = self._receive_packet()
		if not packet or packet[4] == "e":
			return packet, False
		while packet[2] != "l":
			packet = self._receive_packet()
			if not packet or packet[4] == "e":
				return packet, False
		if not self._send_packet("s", "j#js", self.id, login_key, "en"):
			return None, False
		if not confirmation:
			while packet[2] != "js":
				packet = self._receive_packet()
				if not packet or packet[4] == "e":
					return packet, False
		if self.log:
			print "Joined server"
		return packet, True

	def _game(self):
		thread = threading.Thread(target = self._heartbeat)
		thread.start()
		while True:
			packet = self._receive_packet()
			if not packet:
				break
			op = packet[2]
			if op == "e":
				pass
			elif op == "h":
				pass
			elif op == "lp":
				penguin = Penguin.from_player(packet[4])
				self.penguins[penguin.id] = penguin
				self.coins = int(packet[5])
				safemode = packet[6] == '1'
				# egg_timer = int(packet[7])
				login_time = long(packet[8])
				age = int(packet[9])
				# banned_age = int(packet[10])
				play_time = int(packet[11])
				if packet[12]:
					member_left = int(packet[12])
				else:
					member_left = 0
				timezone = int(packet[13])
				# opened_playcard = packet[14] == '1'
				# saved_map_category = int(packet[15])
				# status_field = int(packet[16])
			elif op == "ap":
				penguin = Penguin.from_player(packet[4])
				self.penguins[penguin.id] = penguin
			elif op == "jr":
				self.internal_room_id = int(packet[3])
				self.room_id = int(packet[4])
				self.penguins.clear()
				for i in packet[5:-1]:
					penguin = Penguin.from_player(i)
					self.penguins[penguin.id] = penguin
			elif op == "rp":
				id = int(packet[4])
				if id in self.penguins:
					penguin = self.penguins.pop(id)
				if self.followed and id == self.followed["id"]:
					self._send_packet("s", "b#bf", id)
			elif op == "br":
				id = int(packet[4])
				name = packet[5]
				if raw_input("Buddy with " + name + "? [y/n]") == "y":
					self._send_packet("s", "b#ba", id)
			elif op == "bf":
				room = int(packet[4])
				if self.followed:
					self.join_room(room)
			elif op == "upc":
				id = int(packet[4])
				if id in self.penguins:
					penguin = self.penguins[id]
					color = int(packet[5])
					penguin.clothes["color"] = color
					if self.followed and id == self.followed["id"]:
						self.update_color(color)
			elif op == "uph":
				id = int(packet[4])
				if id in self.penguins:
					penguin = self.penguins[id]
					head = int(packet[5])
					penguin.clothes["head"] = head
					if self.followed and id == self.followed["id"]:
						self.update_head(head)
			elif op == "upf":
				id = int(packet[4])
				if id in self.penguins:
					penguin = self.penguins[id]
					face = int(packet[5])
					penguin.clothes["face"] = face
					if self.followed and id == self.followed["id"]:
						self.update_face(face)
			elif op == "upn":
				id = int(packet[4])
				if id in self.penguins:
					penguin = self.penguins[id]
					neck = int(packet[5])
					penguin.clothes["neck"] = neck
					if self.followed and id == self.followed["id"]:
						self.update_neck(neck)
			elif op == "upb":
				id = int(packet[4])
				if id in self.penguins:
					penguin = self.penguins[id]
					body = int(packet[5])
					penguin.clothes["body"] = body
					if self.followed and id == self.followed["id"]:
						self.update_body(body)
			elif op == "upa":
				id = int(packet[4])
				if id in self.penguins:
					penguin = self.penguins[id]
					hand = int(packet[5])
					penguin.clothes["hand"] = hand
					if self.followed and id == self.followed["id"]:
						self.update_hand(hand)
			elif op == "upe":
				id = int(packet[4])
				if id in self.penguins:
					penguin = self.penguins[id]
					feet = int(packet[5])
					penguin.clothes["feet"] = feet
					if self.followed and id == self.followed["id"]:
						self.update_feet(feet)
			elif op == "upl":
				id = int(packet[4])
				if id in self.penguins:
					penguin = self.penguins[id]
					pin = int(packet[5])
					penguin.clothes["pin"] = pin
					if self.followed and id == self.followed["id"]:
						self.update_pin(pin)
			elif op == "upp":
				id = int(packet[4])
				if id in self.penguins:
					penguin = self.penguins[id]
					background = int(packet[5])
					penguin.clothes["background"] = background
					if self.followed and id == self.followed["id"]:
						self.update_background(background)
			elif op == "sp":
				id = int(packet[4])
				if id in self.penguins:
					penguin = self.penguins[id]
					penguin.x = int(packet[5])
					penguin.y = int(packet[6])
					if self.followed and id == self.followed["id"]:
						self.walk(penguin.x + self.followed["dx"], penguin.y + self.followed["dy"])
			elif op == "sa":
				id = int(packet[4])
				if id in self.penguins:
					action = int(packet[5])
					if self.followed and id == self.followed["id"]:
						self._action(action)
			elif op == "sf":
				id = int(packet[4])
				if id in self.penguins:
					penguin = self.penguins[id]
					penguin.frame = int(packet[5])
					if self.followed and id == self.followed["id"]:
						self._frame(penguin.frame)
			elif op == "sb":
				id = int(packet[4])
				x = int(packet[5])
				y = int(packet[6])
				if self.followed and id == self.followed["id"]:
					self.snowball(x, y)
			elif op == "sm":
				id = int(packet[4])
				msg = packet[5]
				if self.followed and id == self.followed["id"]:
					if self.followed["commands"] and msg.startswith('!'):
						cmd = msg.split(' ')
						name = cmd[0][1:]
						params = cmd[1:]
						self._command(name, params)
					else:
						self.say(msg, False)
			elif op == "ss":
				id = int(packet[4])
				msg = packet[5]
				if self.followed and id == self.followed["id"]:
					self.say(msg, True)
			elif op == "sj":
				id = int(packet[4])
				joke = int(packet[5])
				if self.followed and id == self.followed["id"]:
					self.joke(joke)
			elif op == "se":
				id = int(packet[4])
				emote = int(packet[5])
				if self.followed and id == self.followed["id"]:
					self.emote(emote)
			elif op == "ms":
				coins = int(packet[4])
				cost = self.coins - coins
				self.coins = coins
				sent = packet[5]
				if sent == "0":
					print "Maximum postcards reached"
				elif sent == "1":
					print "Sent postcard successfully (cost " + str(cost) + " coins)"
				elif sent == "2":
					print "Not enough coins"
			elif op == "ai":
				id = int(packet[4])
				coins = int(packet[5])
				cost = self.coins - coins
				self.coins = coins
				msg = "Added item " + str(id) + " (cost " + str(cost) + " coins)"
				if self.followed and self.followed["commands"]:
					self.say(msg)
				if self.log:
					print msg
			elif op == "zo":
				coins = int(packet[4])
				earn = coins - self.coins
				self.coins = coins
				msg = "Earned " + str(earn) + " coins"
				if self.followed and self.followed["commands"]:
					self.say(msg)
				if self.log:
					print msg
			elif self.log:
				print "# UNKNOWN OPCODE: " + op
				
	def _heartbeat(self):
		threading.Timer(600, self._heartbeat)
		self._send_packet("s", "u#h")

	def _command(self, name, params):
		if name == "ai":
			if params:
				self.add_item(params[0])
		elif name == "ac":
			if params:
				self.add_coins(params[0])
		elif name == "ping":
			self.say("pong")

	def connect(self, user, password, encrypted=False, ver=153):
		if self.log:
			print "Connecting to login server at " + self.login_ip + ":" + str(self.login_port) + "..."
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.sock.connect((self.login_ip, self.login_port))
		except:
			return -1
		
		packet, ok = self._login(user, password, encrypted, ver)
		if not ok:
			if packet:
				return int(packet[4])
			return -1
		
		if '|' in packet[4]:
			user = packet[4]
			data = packet[4].split('|')
			self.id = int(data[0])
			# swid = data[1]
			# user = data[2]
			login_key = data[3]
			# ??? = data[4]
			# language_approved = int(data[5])
			# language_rejected = int(data[6])
			# ??? = data[7] == "true"
			# ??? = data[8] == "true"
			# ??? = int(data[9])
			confirmation = packet[5]
			# friends_login_key = packet[6]
			# ??? = packet[7]
			# email = packet[8]
		else:
			self.id = int(packet[4])
			login_key = packet[5]
			confirmation = None
		
		if self.log:
			print "Connecting to game server at " + self.game_ip + ":" + str(self.game_port) + "..."
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.sock.connect((self.game_ip, self.game_port))
		except:
			return -2
		
		packet, ok = self._join_server(user, login_key, confirmation, ver)
		if not ok:
			if packet:
				return int(packet[4])
			return -2
		
		thread = threading.Thread(target=self._game)
		thread.start()
		return 0

	def get_penguin_id(self, name):
		for penguin in self.penguins.values():
			if penguin.name == name:
				return penguin.id
		return 0

	def join_room(self, id, x = 0, y = 0):
		if self.log:
			print "Joining room " + str(id) + "..."
		self._send_packet("s", "j#jr", id, x, y)

	def join_igloo(self, id):
		if self.log:
			print "Joining " + str(id)+ "'s igloo..."
		self._send_packet("s", "j#jp", None, self.id, int(id) + 1000)

	def update_color(self, id):
		if self.log:
			print "Changing color to " + str(id) + "..."
		self._send_packet("s", "s#upc", id)

	def update_head(self, id):
		if self.log:
			print "Changing head item to " + str(id) + "..."
		self._send_packet("s", "s#uph", id)

	def update_face(self, id):
		if self.log:
			print "Changing face item to " + str(id) + "..."
		self._send_packet("s", "s#upf", id)

	def update_neck(self, id):
		if self.log:
			print "Changing neck item to " + str(id) + "..."
		self._send_packet("s", "s#upn", id)

	def update_body(self, id):
		if self.log:
			print "Changing body item to " + str(id) + "..."
		self._send_packet("s", "s#upb", id)

	def update_hand(self, id):
		if self.log:
			print "Changing hand item to " + str(id) + "..."
		self._send_packet("s", "s#upa", id)

	def update_feet(self, id):
		if self.log:
			print "Changing feet item to " + str(id) + "..."
		self._send_packet("s", "s#upe", id)

	def update_pin(self, id):
		if self.log:
			print "Changing pin to " + str(id) + "..."
		self._send_packet("s", "s#upl", id)

	def update_background(self, id):
		if self.log:
			print "Changing background to " + str(id) + "..."
		self._send_packet("s", "s#upp", id)
		
	def walk(self, x, y):
		if self.log:
			print "Walking to (" + str(x) + ", " + str(y) + ")..."
		self._send_packet("s", "u#sp", None, self.id, x, y)
		
	def _action(self, id):
		self._send_packet("s", "u#sa", id)
		
	def _frame(self, id):
		self._send_packet("s", "u#sf", id)
		
	def dance(self):
		if self.log:
			print "Dancing..."
		self._frame(26)

	def wave(self):
		if self.log:
			print "Waving..."
		self._action(25)
		
	def sit(self, dir = "s"):
		if self.log:
			print "Sitting..."
		dirs = {
			"se": 24,
			"e": 23,
			"ne": 22,
			"n": 21,
			"nw": 20,
			"w": 19,
			"sw": 18,
			"s": 17
		}
		if dir in dirs:
			self._frame(dirs[dir])
		else:
			self._frame(dirs["s"])

	def snowball(self, x, y):
		if self.log:
			print "Throwing snowball to (" + str(x) + ", " + str(y) + ")..."
		self._send_packet("s", "u#sb", x, y)

	def say(self, msg, safe = False):
		if self.log:
			print "Saying '" + msg + "'..."
		if safe:
			self._send_packet("s", "u#ss", msg)
		else:
			self._send_packet("s", "m#sm", self.id, msg)

	def joke(self, joke):
		if self.log:
			print "Saying joke " + str(joke) + "..."
		self._send_packet("s", "u#sj", None, self.id, joke)
		
	def emote(self, emote):
		if self.log:
			print "Reacting emote " + str(emote) + "..."
		self._send_packet("s", "u#se", emote)

	def mail(self, id, postcard):
		if self.log:
			print "Sending postcard #" + str(postcard) + "..."
		self._send_packet("s", "l#ms", id, postcard)
	
	def add_item(self, id):
		if self.log:
			print "Adding item " + str(id) + "..."
		self._send_packet("s", "i#ai", id)

	def add_coins(self, coins):
		if self.log:
			print "Adding " + str(coins) + " coins..."
		room = self.room_id
		self.join_room(912)
		self._send_packet("z", "zo", coins)
		self.join_room(room)

	def add_stamp(self, id):
		if self.log:
			print "Adding stamp " + str(id) + "..."
		self._send_packet("s", "st#sse", id)
	
	def add_igloo(self, id):
		if self.log:
			print "Adding igloo " + str(id) + "..."
		self._send_packet("s", "g#au", None, self.id, id)

	def music(self, id):
		if self.log:
			print "Setting music to #" + str(id) + "..."
		self._send_packet("s", "g#go", None, self.id)
		self._send_packet("s", "g#um", None, self.id, id)

	def add_furniture(self, id):
		if self.log:
			print "Adding furniture " + str(id) + "..."
		self._send_packet("s", "g#af", id)

	def buddy(self, id):
		if self.log:
			print "Sending buddy request to " + str(id) + "..."
		self._send_packet("s", "b#br", id)

	def follow(self, name, dx = 0, dy = 0, commands = False):
		if self.log:
			print "Following " + name + "..."
		id = self.get_penguin_id(name)
		if id:
			self.buddy(id)
			self.followed = {"id": id, "dx": dx, "dy": dy, "commands": commands}
			penguin = self.penguins[id]
			self.walk(penguin.x + dx, penguin.y + dy)
			self.update_color(penguin.clothes["color"])
			self.update_head(penguin.clothes["head"])
			self.update_face(penguin.clothes["face"])
			self.update_neck(penguin.clothes["neck"])
			self.update_body(penguin.clothes["body"])
			self.update_hand(penguin.clothes["hand"])
			self.update_feet(penguin.clothes["feet"])
			self.update_pin(penguin.clothes["pin"])
			self.update_background(penguin.clothes["background"])

	def unfollow(self):
		if self.log:
			print "Unfollowing..."
		self.followed = None

	def logout(self):
		if self.log:
			print "Logging out..."
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()
