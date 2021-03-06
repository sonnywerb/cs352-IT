from socket import *
import sys
import binascii
import struct

#From James Routley's blog post about DNS messages, posted on Sakai
def send_udp_message(message, address, port):
    """send_udp_message sends a message to UDP server

    message should be a hexadecimal encoded string
    """
    message = message.replace(" ", "").replace("\n", "")
    server_address = (address, port)

    sock = socket(AF_INET, SOCK_DGRAM)
    try:
        sock.sendto(message, server_address)
        #sock.sendto(binascii.unhexlify(message), server_address)
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    return binascii.hexlify(data).decode("utf-8")


def format_hex(hex):
    """format_hex returns a pretty version of a hex string"""
    octets = [hex[i:i+2] for i in range(0, len(hex), 2)]
    pairs = [" ".join(octets[i:i+2]) for i in range(0, len(octets), 2)]
    return "\n".join(pairs)

##############################################

#From tigerlyb's DNS lookup tool
def makeDNSQuery(domain):
	d = ""
	for a in domain.split('.'):
		d = d + struct.pack("!b" + str(len(a)) + 's', len(a), bytes(a) )
	
	l1 = "\x41\x41"
	l2 = "\x01\x00"
	l3 = "\x00\x01"
	l4 = "\x00\x00"
	l5 = "\x00\x00"
	l6 = "\x00\x00"
	header = l1 +l2 + l3 + l4 + l5 + l6
	q = d + "\x00\x00\x01\x00\x01"
	m = header + q
	print("----DNS query:----") #Debug
	print(format_hex(m.encode("hex") ) ) #Also debug
	return m
###############################################

#I reverse engineered Routley's format hex code in order to write a function that gives an IP address in decimal
def getIPAddress(hex):
	quartets = [ hex[i:i+2] for i in range(len(hex)-8, len(hex), 2) ] #convert into a series of hex characters, then group the last 8 characters into pairs
	i=0
	while i<4:
		quartets[i]=str( int(quartets[i], 16) ) #convert from hex to decimal, then cast the result into a string
		i=i+1
	return ".".join(quartets)

###############################################

# Server socket
server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind( ('', int(sys.argv[1]) ) )
server_sock.listen(1)
print("The server is ready to receive!")
message, clientAddr = server_sock.accept()#The client uses TCP, but I will not do this in UDP


while True:
	url = message.recv(256).decode('utf-8')
	if not url: # if I don't get anything from the client
		break
	
	print("This is the URL: " + url) #Debug
	query = makeDNSQuery(url)
	response = send_udp_message(query, "8.8.8.8", 53) #Google's DNS server
	print("----This is the server's response:----") #Debug
	print(format_hex(response) ) #Debug
	ipAddress = getIPAddress(response)
	print("ipAddress is: " + ipAddress) #Debug
	message.send(ipAddress.encode('utf-8') )

print("Server shutting down")
message.close()
server_sock.close()

