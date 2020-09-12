#Abraham Gale 2020
#feel free to add functions to this part of the project, just make sure that the get_dns_response function works
from resolver_backround import DnsResolver
import threading
import socket
import struct
import argparse
from sys import argv
from time import sleep
from helper_funcs import DNSQuery

def make_sock(question, addr, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (addr, port)
	sock.sendto(question.to_bytes, server_address)
	answer = sock.recv(1024)
	return answer


class MyResolver(DnsResolver):
	def __init__(self, port):
		self.port = port
		self.sname
		self.stype
		self.sclass
		self.slist = []
		self.sbelt = ["172.16.7.7", "128.6.1.1", "198.41.0.4"] #I was told to hardcode that
		self.cache = {
			"A": None, #ip address
			"NS": None, #name server
			"CNAME": None, #canonical name
		}
		self.cache_lock = threading.Lock()
		
	def get_dns_response(self, query):
		#input: A query and any state in self
		#returns: the correct response to the query obtained by asking DNS name servers
		#Your code goes here, when you change any 'self' variables make sure to use a lock
		q = DNSQuery(query)
		print(q)
		
		with self.cache_lock:
			self.stype = q.question["QTYPE"]
			self.sclass = q.question["QCLASS"]
			self.sname = q.question["NAME"]
		
		a = DNSQuery()
		a.header['ID'] = q.header['ID']
		a.header['QR'] = 1
		a.header['RCODE'] = 2
		while True:
			#1. Check if answer in cache
			if self.cache["A"] != None:
				a.answer['RDATA']=self.cache["A"]
			
			#2. Find name server (NS) in cache if I can't find the answer, starting with SNAME, then parent domain, grandparent, etc
			#	Ex: If SNAME is mockapetris.isi.edu, I would try mockapetris.isi.edu, then isi.edu, then edu, and finally . (dot)
			if self.cache["NS"] != None:
				ns = self.cache["NS"]
			else:
				#NS search failed, try SBELT instead
				for addr in self.sbelt:
					#if succeed, break
			
			#3. Query name servers
			ns_call = make_sock(ns, 53 ,self.port)
			response = DNSQuery(ns_call)
		
			#4. 4 possible cases:
			#a. If the case is a type A or a name error, cache it and go to step 1 (I've found something!)
			#b. If I find a new NS answer, cache that answer and go to step 2
			#c. If I find a CNAME that isn't the answer, cache the CNAME, change SNAME to the canon name in CNAME RR and go to step 1
			#d. If error, delete that server from server list slist and go to step 3
			
			#NOTE:
			#If A, then QTYPE=1
			#IF NS, then QTYPE=2
			#If CNAME, then QTYPE=5
			with self.cache_lock:
				if response.answers.[0]["TYPE"] == 1:
					self.cache["A"] = response
				if response.answers.[0]["TYPE"] == 2:
					self.cache["NS"] = response
				if response.answers.[0]["TYPE"] == 5:
					self.cache["CNAME"] = response
					self.sname = response.answers.[0]["RDATA"]
				else:
		
		print(a)
		return a.to_bytes()
		
		
parser = argparse.ArgumentParser(description="""This is a DNS resolver""")
parser.add_argument('port', type=int, help='This is the port to connect to the resolver on',action='store')
args = parser.parse_args(argv[1:])
resolver = MyResolver(args.port)
resolver.wait_for_requests()
