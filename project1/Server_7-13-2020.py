from socket import *
import sys
import binascii

#from James Routley's blog post about DNS messages, posted on Sakai
def send_udp_message(message, address, port):
    """send_udp_message sends a message to UDP server

    message should be a hexadecimal encoded string
    """
    message = message.replace(" ", "").replace("\n", "")
    server_address = (address, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(binascii.unhexlify(message), server_address)
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    return binascii.hexlify(data).decode("utf-8")


def format_hex(hex):
    """format_hex returns a pretty version of a hex string"""
    octets = [hex[i:i+2] for i in range(0, len(hex), 2)]
    pairs = [" ".join(octets[i:i+2]) for i in range(0, len(octets), 2)]
    return "\n".join(pairs)
###############################################


# Server socket
server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind( ('', int(sys.argv[1]) ) )
server_sock.listen(1)
print("The server is ready to receive!")
message, clientAddr = server_sock.accept()#The client uses TCP, but I will not do this in UDP

while True:
	orgStr = message.recv(256).decode('utf-8')
	if not orgStr: # if I don't get anything from the client
		break
	print("This is the URL: " + orgStr)
	message = "AA AA 01 00 00 01 00 00 00 00 00 00 " \
	"07 65 78 61 6d 70 6c 65 03 63 6f 6d 00 00 01 00 01"
	#"example.com"
	#I would like to generalize the message string for *any* URL the client sends
	print("This is the string that will be sent to the DNS server: " + message)
	response = send_udp_message(message, "8.8.8.8", 53) #Google's DNS server
	print("This is the server's response: " + response)
	ipAddress = "12.345.678.90" #Placeholder
	message.send(ipAddress.encode('utf-8') )

print("Server shutting down")
message.close()
server_sock.close()

