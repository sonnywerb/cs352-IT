from socket import *
import sys

# Server socket
server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind( ('', int(sys.argv[1]) ) )
server_sock.listen(1)
print("The server is ready to receive!")
message, clientAddr = server_sock.accept()

while True:
	orgStr = message.recv(256).decode('utf-8')
	if not orgStr: # if I don't get anything from the client
		break
	# Reverse string
	print('--Input: ' + orgStr)
	reversedStr = ''.join(reversed(orgStr) )
	print('--Output: ' + reversedStr)
	#
	message.send(reversedStr.encode('utf-8') )

print("Server shutting down")
message.close()
server_sock.close()

