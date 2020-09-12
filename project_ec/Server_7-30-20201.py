import argparse
from sys import argv
import socket
from helper_funcs import DNSQuery
from random import randint
import binascii

def process_dns(line, sock):
	inputLine=line.split() #Need to separate URL from type
	print("This is the input:", inputLine)
	
	q = DNSQuery()
	
	#If A, then QTYPE=1
	#IF NS, then QTYPE=2
	#If CNAME, then QTYPE=5
	#If MX, then QTYPE=15
	#If TXT, then QTYPE=16
	#Everything else is assumed to be unknown
	if inputLine[1]=='A':
		q.question['QTYPE'] = 1
	elif inputLine[1]=='NS':
		q.question['QTYPE'] = 2
	elif inputLine[1]=='CNAME':
		q.question['QTYPE'] = 5
	elif inputLine[1]=='MX':
		q.question['QTYPE'] = 15
	elif inputLine[1]=='TXT':
		q.question['QTYPE'] = 16
	else:
		if "TYPE" in inputLine[1]:
			typeNo=int (inputLine[1][4:])
			q.question['QTYPE']=typeNo
			print("NOTICE: Since you entered TYPE<number> into your input, I will assume this is an unknown type, EVEN IF it's actually a type that was mentioned in the prompt")
		else:
			return "ERROR"
	print(q.question)
	
	#I assume everything else in the question will not change
	q.question['QCLASS'] = 1
	q.question['NAME'] = inputLine[0].encode('ASCII')
	q.header['QDCOUNT'] = 1
	q.header['RD'] = 1
	q.header['ID'] = randint(0, 65535)
	sock.send(q.to_bytes())
	answer = sock.recv(512)
	outputStr = ""
	
	#Now to deal with the answers
	a = DNSQuery(answer)
	#print(a.answers)#Oh god
	ip_list = []

	
	if inputLine[1]=='A':
		for data in a.answers:
			if data['TYPE'] != 1:
				ip_list.append('Not found!') #For some reason, I still will get that one type A request that isn't a type A. I cannot control this
			else:
				ip_list.append('.'.join([str(int(item) ) for item in data['RDATA'][0] ]) )
				
		for i, addr in enumerate(ip_list):
			outputStr = outputStr+inputLine[0]+". IN A "+addr
			if i<len(ip_list)-1:
				outputStr = outputStr+"\n"
			
		#outputStr = ', '.join(ip_list)
		#outputStr = inputLine[0]+". IN A "+outputStr
	
	elif inputLine[1]=='NS':
		for data in a.answers:
			ip_list.append(data['RDATA'][0].decode("ASCII") )
			
		for i, addr in enumerate(ip_list):
			outputStr = outputStr+inputLine[0]+". IN NS "+addr
			if i<len(ip_list)-1:
				outputStr = outputStr+"\n"
	
	elif inputLine[1]=='CNAME':
		for data in a.answers:
			ip_list.append(data['RDATA'][0].decode("ASCII") )
			
		for i, addr in enumerate(ip_list):
			outputStr = outputStr+inputLine[0]+". IN CNAME "+addr
			if i<len(ip_list)-1:
				outputStr = outputStr+"\n"
	
	elif inputLine[1]=='MX':
		num_list = []
		for data in a.answers:
			num_list.append(str(int.from_bytes(data['RDATA'][0], 'big') ) )
			ip_list.append(data['RDATA'][1].decode("ASCII") )
			
		for i, addr in enumerate(ip_list):
			outputStr = outputStr+inputLine[0]+". IN MX "+num_list[i]+" "+addr
			if i<len(ip_list)-1:
				outputStr = outputStr+"\n"#Order stops mattering, so I just print whichever comes first
	
	elif inputLine[1]=='TXT':
		for data in a.answers:
			ip_list.append(data['RDATA'][0].decode("utf-8") )
			
		for i, addr in enumerate(ip_list):
			outputStr = outputStr+inputLine[0]+". IN TXT "+addr
			if i<len(ip_list)-1:
				outputStr = outputStr+"\n"#Again, order doesn't matter
	
	else:
		for data in a.answers:
			res="".join([format(item, '02x') for item in data['RDATA'][0] ]) #Each item will have 2 digits, so it keeps the leading zero
			outputStr = inputLine[0]+". IN "+inputLine[1]+" \# "+str(data['RDLENGTH'])+" "+res
	
	print("This is the result:\n")
	print(outputStr)
	print("\n")
	return outputStr


#First we use the argparse package to parse the aruments
parser=argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('port', type=int, help='This is the port to open the server on',action='store')
args = parser.parse_args(argv[1:])

#next we create a server socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('', args.port)
server_sock.bind(server_addr)
server_sock.listen(0)
print("The server is ready to receive!")
new_sock, addr = server_sock.accept()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('',  args.port + 1))
sock.connect(('8.8.8.8', 53))
#now we need to reverse whatever is sent to us
#first set close condition to False
done = False
while not done:
		#now we return the reversed line whenever it is sent to us
		line = new_sock.recv(256)
		#check if done
		if not line:
			done = True
			continue
		line = line.decode('utf-8')
		#now do the magic
		line = process_dns(line, sock)
		if not line:
			line = 'Not Found'
		new_sock.sendall(line.encode('utf-8'))




#close the sockets
print("Server shutting down")
new_sock.close()
server_sock.close()
sock.close()
