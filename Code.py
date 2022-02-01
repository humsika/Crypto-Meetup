import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey , X25519PublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey, Ed25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend

from Crypto.Cipher import AES
import ast

def b64(msg):
    return base64.encodebytes(msg).decode('utf-8').strip()

def hkdf(inp, length):
    hkdf = HKDF(algorithm=hashes.SHA256(), length=length, salt=b'',info=b'', backend=default_backend())
    return hkdf.derive(inp)

def pad(msg):
    num = 16 - (len(msg) % 16)
    return msg + bytes([num] * num)

def unpad(msg):
    return msg[:-msg[-1]]

def serialize(dic,single=False):
	if (single==True):
		dic = dic.public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
		return dic
	for key in dic:
		dic[key] = dic[key].public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw) if dic[key] else None
	return str(dic).encode("utf-8")
def unserialize(dic,single=False):
	if (single):
		dic = X25519PublicKey.from_public_bytes(dic)
		return dic
	dic = ast.literal_eval(dic.decode("utf-8"))
	for key in dic:
		dic[key] = X25519PublicKey.from_public_bytes(dic[key]) if dic[key] else None
	return dic

class SymmRatchet(object):
    def __init__(self, key):
        self.state = key

    def next(self, inp=b''):
        output = hkdf(self.state + inp, 80)
        self.state = output[:32]
        outkey, iv = output[32:64], output[64:]
        return outkey, iv

class Bob(object):
    def __init__(self):
        self.IKb = X25519PrivateKey.generate()
        self.SPKb = X25519PrivateKey.generate()
        self.OPKb = X25519PrivateKey.generate()
        self.DHratchet = X25519PrivateKey.generate()
        self.other = None

    def x3dh(self):
        dh1 = self.SPKb.exchange(self.other["IKa"])
        dh2 = self.IKb.exchange(self.other["EKa"])
        dh3 = self.SPKb.exchange(self.other["EKa"])
        dh4 = self.OPKb.exchange(self.other["EKa"])
        self.sk = hkdf(dh1 + dh2 + dh3 + dh4, 32)
        
        

    def init_ratchets(self):
        self.root_ratchet = SymmRatchet(self.sk)
        self.recv_ratchet = SymmRatchet(self.root_ratchet.next()[0])
        self.send_ratchet = SymmRatchet(self.root_ratchet.next()[0])

    def dh_ratchet(self):
        dh_recv = self.DHratchet.exchange(self.other["DHratchet"])
        shared_recv = self.root_ratchet.next(dh_recv)[0]
        self.recv_ratchet = SymmRatchet(shared_recv)
        self.DHratchet = X25519PrivateKey.generate()
        dh_send = self.DHratchet.exchange(self.other["DHratchet"])
        shared_send = self.root_ratchet.next(dh_send)[0]
        self.send_ratchet = SymmRatchet(shared_send)
        

    def send(self, msg):
        key, iv = self.send_ratchet.next()
        cipher = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(msg))
       	return cipher

    def recv(self, cipher , flag):
        if flag:
            self.dh_ratchet()
        key, iv = self.recv_ratchet.next()
        msg = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(cipher))
        return msg

class Alice(object):
    def __init__(self):
        self.IKa = X25519PrivateKey.generate()
        self.EKa = X25519PrivateKey.generate()
        self.DHratchet = None
        self.other = None

    def x3dh(self):
        dh1 = self.IKa.exchange(self.other["SPKb"])
        dh2 = self.EKa.exchange(self.other["IKb"])
        dh3 = self.EKa.exchange(self.other["SPKb"])
        dh4 = self.EKa.exchange(self.other["OPKb"])
        self.sk = hkdf(dh1 + dh2 + dh3 + dh4, 32)
        
        
    def init_ratchets(self):
        self.root_ratchet = SymmRatchet(self.sk)
        self.send_ratchet = SymmRatchet(self.root_ratchet.next()[0])
        self.recv_ratchet = SymmRatchet(self.root_ratchet.next()[0])

    def dh_ratchet(self):
        if self.DHratchet is not None:
            dh_recv = self.DHratchet.exchange(self.other["DHratchet"])
            shared_recv = self.root_ratchet.next(dh_recv)[0]
            self.recv_ratchet = SymmRatchet(shared_recv)
        self.DHratchet = X25519PrivateKey.generate()
        dh_send = self.DHratchet.exchange(self.other["DHratchet"])
        shared_send = self.root_ratchet.next(dh_send)[0]
        self.send_ratchet = SymmRatchet(shared_send)
        
    def send(self, msg):
        key, iv = self.send_ratchet.next()
        cipher = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(msg))
        return cipher
        
    def recv(self, cipher,flag):
        if flag:
            self.dh_ratchet()
        key, iv = self.recv_ratchet.next()
        msg = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(cipher))
        return msg






















