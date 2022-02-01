# importing required modules
import threading , socket , smtplib , string , random , sys , os , pickle , ast , time
from Code import *
# email login
class Mail:
	def __init__(self,mail,passwd):
		self.mail = mail
		self.passwd = passwd
		self.server = smtplib.SMTP("smtp.gmail.com",587)
		self.server.ehlo()
		self.server.starttls()
		self.server.ehlo()
		self.server.login(self.mail,self.passwd)
	def send(self,recv,key):
		try:
			text = f"This is Johny#som37h1ng your OTP is {key}"
			subject = "Hey , there"
			message = """\
			From: %s
			To: %s
			Subject: %s

%s
			""" % (self.mail,recv,subject,text)
			self.server.sendmail(self.mail,recv,message)
			return 1
		except smtplib.SMTPRecipientsRefused :
			print("error")
			return 0
# creating server
class Server:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creating Socket
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.pub_bob = {}
		self.pub_alice = {}
		self.connections = {}
		self.email = Mail(os.getenv("MAIL"),os.getenv("MAIL_PASSWORD")) # taking mail and password from system for loggin in
		self.ip = "127.0.0.1" # Local Ip
		self.sock.bind((self.ip,8000)) # Binding connection
		self.sock.listen(1)
		print("Server Created Successfully...")
	def  handler(self,c,a):
		while True:
			data = c.recv(1024)
			for connection in self.connections:
				if connection != c:
					connection.send(data)	
			if not data:
				print(self.connections[c] + " is disconnected")
				del self.connections[c]
				c.close()
				break

	def Run(self,c,a):
		user = None
		if len(self.connections) <= 1:
			if (len(self.connections)==0):
				user = "0"
			else:
				user = "1"
			c.send(bytes(user,"utf-8"))
			self.Id = str(c.recv(7),"utf-8")
			# Generating Random Token
			key = ''.join([random.choice(string.ascii_letters + string.digits ) for n in range(random.randint(11,15))]) 
			print(key)
			# Sending Key to user mail , if the mail in incorrect then displaying error message to the user and close the connection
			mail_sent = self.email.send(self.Id+"@rguktn.ac.in",key)
			if not mail_sent:
				c.send(bytes("Invalid mail...","utf-8"))
				c.close()
				return
			c.send(bytes("Please Check Your Mail !...","utf-8")) 
			self.token = None # initially token is empty
			i = 0 # incorrect count
			Verified = False # initially Verified in False
			# if the user enters an incorrect token 3 times then displays an error message
			while ( i < 3 ):
				self.token = str(c.recv(100),"utf-8") # receiving token from user
				if (self.token == key): # checking if the received token is the generated key or not
					c.send(bytes("Verified","utf-8")) # Sending Verified message to the user
					Verified = True 
					break # back out from loop
				c.send(bytes("Incorrect","utf-8")) # Sending Incorrect message to client
				self.token = None
				i+=1
			if (Verified == False): # If the user is not Verified(i.e token is incorrect 3 times) then close the connection.
				c.close()
				return

			public = unserialize(c.recv(10000))
			if user == "0":
				self.pub_bob = public
			elif user == "1":
				self.pub_alice = public
				time.sleep(10)
				c.send(bytes("init","utf-8"))
				c.send(serialize(self.pub_bob))
				self.pub_alice = unserialize(c.recv(10000))
				for connection in self.connections:
					if connection != c:
						connection.send(bytes("init","utf-8"))
						connection.send(serialize(self.pub_alice))		


			# Creating Threading for taking messages from users and sending it to remaining users 
			athread = threading.Thread(target = self.handler,args = (c,a))
			athread.daemon = True # background task
			athread.start() # Starting thread
			self.connections[c] = self.Id # adding user to connectoins list
			print( self.connections[c] + " is connected.")
		else:
			c.send(bytes("False","utf-8"))
			c.close()
	def run(self):
		while True:
			c,a = self.sock.accept() # accepting connections from user
			# Creating Threading for connecting multiple users at a time.
			bthread = threading.Thread(target= self.Run,args=(c,a))	
			bthread.daemon = True # background task
			bthread.start() # Starting Thread
# Starting Server 
S = Server()
S.run()