# importing required modules
import threading , socket , os
from Code import *
import ast
class Client:
	# Creating Socket
	user = None
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	def sendmess(self): # Sending Message
		while True:
			msg = input("You   : ")
			data = {"msg":self.user.send(bytes(msg,"utf-8")),"DHratchet":serialize(self.user.DHratchet.public_key(),True)}
			self.sock.send(str(data).encode("utf-8"))
	def recvmess(self): # Receiving message
		while True:
			data = self.sock.recv(1024)
			if not data:
				break
			data = ast.literal_eval(data.decode("utf-8"))
			flag = False
			if self.user.other["DHratchet"] is None or serialize(self.user.other["DHratchet"],True) != data["DHratchet"]:
				self.user.other["DHratchet"] = unserialize(data["DHratchet"],True)
				flag = True
			msg = self.user.recv(data["msg"],flag)
			print("\b\b\b\b\b\b\b\b\bOther : " + msg.decode("utf-8") + "\n" + "You   : ",end="")
	def initialize(self):
		self.user.other = unserialize(self.sock.recv(10000))
		self.user.x3dh()
		self.user.init_ratchets()
		self.user.dh_ratchet()
	def __init__(self):
		# Local Ip
		self.ip = "127.0.0.1"
		try:
			# Connect to Server
			self.sock.connect((self.ip,8000))
		except:
			print("Server not Established.") # If there is an error in the connection , then displaying error message
			exit(0)
		allow = str(self.sock.recv(100),'utf-8')
		if allow == "False":
			print("Not reachable")
			exit(0)
		# Taking Id from user , based on Id the token is generated and send token to user mail
		self.Id = input("Id: ")
		# sending Id to server
		self.sock.send(bytes(self.Id,"utf-8"))
		# Receiving message from server
		print(str(self.sock.recv(100),"utf-8"))
		# incorrect count
		i = 1
		Verified = False
		while True: # infinite loop until the break statement
			token = input("Enter Key: ") # taking token from user which is sent to mail
			self.sock.send(bytes(token,"utf-8")) # sending token to server
			signal = str(self.sock.recv(100),"utf-8")
			if i == 3:
				break
			if (signal == "Incorrect"): # if the user enters incorrect password in 3 times.
				print("Wrong Key.Try again...")
				i += 1
				continue
			Verified = True
			break
		if Verified==False:
			print("S0rry 7ry 4g41n La73r !!!!!!!!!!!!!!!!!!!...")
			exit(0)

		print("\t\t\tLogediIn Successfully...!")

		if allow == '0':
			self.user = Bob()
			public = {"IKb":self.user.IKb.public_key(),"SPKb":self.user.SPKb.public_key(),"OPKb":self.user.OPKb.public_key(),"DHratchet":self.user.DHratchet.public_key() if self.user.DHratchet else None }
			self.sock.send(serialize(public))
		elif(allow == '1'):
			self.user = Alice()
			public = {"IKa":self.user.IKa.public_key(),"EKa":self.user.EKa.public_key(),"DHratchet":self.user.DHratchet.public_key() if self.user.DHratchet else None}
			self.sock.send(serialize(public))
		
		init = self.sock.recv(1000)
		if init:
			self.initialize()
			if isinstance(self.user,Alice):
				public["DHratchet"] = serialize(self.user.DHratchet.public_key(),True)
				self.sock.send(str(public).encode("utf-8"))
			
		# Creating threads
		bthread = threading.Thread(target = self.sendmess)
		bthread.daemon = True
		bthread.start()
		cthread = threading.Thread(target = self.recvmess)
		cthread.start()
# Creating Client Object
client = Client()
