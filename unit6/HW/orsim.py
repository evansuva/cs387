# hw 6
# For simplicity, we use RSA without any padding, even though this would not
# be secure in general.
#
from __future__ import division
import itertools
from bits import *
from Crypto.Random import random
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5
import binascii

class Network(object):
    """Trivial network simulator"""
    def __init__(self):
        self._nodes = {}

    def lookup_node(self, name):
        if name in self._nodes:
            return self._nodes[name]
        return None
        
    def add_node(self, name):
        assert name not in self._nodes
        n = Node(self, name)
        self._nodes[name] = n
        return n

    def get_node(self, name):
        return self._nodes[name]
    
    def send_message(self, src, dest, msg):
        print "send message!"
        snode = self.lookup_node(src)
        dnode = self.lookup_node(dest)
        assert snode
        assert dnode
        dnode.receive(src, msg)

class Node(object):
    def __init__(self, network, name):
        self._network = network
        self.name = name
        prng = Random.new().read
        self.RSA = RSA.generate(1024, prng)

    def get_public_key(self):
        return self.RSA.publickey()
    
    def send(self, msg, dest):
        assert self._network.lookup_node(dest)
#        print "Sending: (%s to %s) %s" % (self.name, dest, msg)
        print "Sending: (%s to %s)" % (self.name, dest)
        self._network.send_message(self.name, dest, msg)

    def process(self, msg):
        print "Processing:", msg
        if msg.startswith("To:"):
            pos = msg.find(":",3)
            assert pos != -1
            dest = msg[3:pos]
            print "dest: ", dest
            rest = msg[pos + 1:]
            self.send(rest, dest)
        else:
            print "Received:", msg
            
    def receive(self, src, msg):
#        print "Received: (%s from %s) %s" % (self.name, src, msg)
        print "Received: (%s from %s)" % (self.name, src)
        plaintext = self.RSA.decrypt(msg)
        rcv = bin_to_string(plaintext)
        self.process(rcv)
        
    def test(self):
        msg = "Hello"
        c0 = self.RSA.encrypt(string_to_hexstring(msg),None)[0]
        m0 = self.RSA.decrypt(c0)
        assert hexstring_to_string(m0) == msg
        print "Passed 1!"
        
        sb = string_to_bin(msg)
        c1 = self.RSA.encrypt(sb,None)[0]
        print "Equal? " + str(c0 == m0)
        m1 = self.RSA.decrypt(c1)
        assert sb == m1
        print "Passed 2!"
        msgx = bin_to_string(m1)
        assert msgx == sb
        
        msg2 = string_to_hexstring("To:A:") + sb
        c2 = self.RSA.encrypt(msg2,None)[0]
        m2 = self.RSA.decrypt(c2)
        assert m2 == msg2
        print "Passed 3!"
        
##        c0 = self.RSA.encrypt(string_to_hexstring(msg),None)[0]
##        m0 = hexstring_to_string(self.RSA.decrypt(c0))
##        msg1 = string_to_hexstring(c0) # "To: A/") + bin_to_hexstring(c0)
##        print "msg1: ", msg1
##        # print "ms: ", hexstring_to_string(msg1)
##        c1 = self.RSA.encrypt(msg1,0)[0]
##        m1 = hexstring_to_string(self.RSA.decrypt(c1))
##        
##        print "m1: ", bin_to_hexstring(m1)
##        assert m1 == msg1

def test():
    network = Network()
    nodes = ["A", "B", "C", "D"]
    keys = {}
    for node in nodes:
        n = network.add_node(node)
        # n.test()
        keys[node] = n.get_public_key()
        
    innermsg = bin_to_string(keys["C"].encrypt(string_to_bin("Hello"),0)[0])
    innermsg = keys["B"].encrypt(string_to_bin("Hello"),0)[0]
    msg = string_to_bin("To:B:") + innermsg
    m0 = keys["B"].encrypt(msg,0)[0]
    network.send_message("A", "B", m0)                                                       
    return network
        
        
