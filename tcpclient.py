''' 
....Author :: 'Saathvik Prasad'....
..
    ....... The program is modified and the base idea of the program was adopted from the project skeleton provided........
* This is the program for client side of the "Multithreaded Server client system.
* The program can be used to ask for a file from the server and the file is sent back 
 to the client if the file exists or the error message file or webpage is displayed to the user.

* The program uses the TCP connection to connect to the server and requests the file.
* The request message is sent to the server using the HTTP message reqest form.(as described in the chapter 2).
* The request message describes the type of method used for the request is using, the file requested, 
 the host and the port number, the agent, connection time, and the 
 language used in the client side application.
* Once the file is received the file is saved on the client side using a 'new_'filename, which is saved in the folder.
* The file is opened in the respective application for the user to view.
* The program is written in python 2.7+ version using Linux mint. The required libraries have been imported in the program.

'''


import socket
import sys

error = '404'			#declare the codes for message interprtation
accept = '200'


'''
Utility function to create a request packet for the client to send to the server.
The request information is encapsulated in the header packet.
'''

def http_req_message(host,port,file_n):
	print "Generating the http request packet.."
	head1 = "GET "+"/"+ file_n +" "+"HTTP/1.1"
	head2 = "Host:"+str(host)+":"+str(port)
	head3 = "User-Agent:Terminal(x11;Ubuntu;Linux x86_64)"
	head4 = "Accept: text/html,application"
	head5 = "Accept-Language:en-US,en;"
	head6 = "Accept ending:gzip,deflate"
	head7 = "Connection:keep-Alive"
	final_req_header = head1+"\n "+head2+"\n "+head3+"\n "+head4+"\n "+head5+"\n "+head6+"\n "+head7
	return final_req_header



'''
Main function..used to create a socket on the client side of the application and to interact with the server for the file.
'''
def Main(host_ip,port_num,client_file):
	host = host_ip																# host number accepted from the user
	port = int(port_num)														# port number of the server side application, accepted from the user

	s = socket.socket()
	s.connect((host,port))														# bind the port to the host, and connect to the server

	filename = client_file
	if filename != 'q':															# if file name is not 'q' (quit),check if user wants to terminate connection.
		req_packet = http_req_message(host,port,filename)						# create packet	
		print "Http packet formed.."
		print "Sending request to the server with filename.."
		s.send(req_packet)														# relay packet to the server
		print "Receiving data from the server.."
		data_back = s.recv(2048)												# receive packet from the server and buffer size is declared as 2048 bytes.
		data_c = data_back.split('\n')
		data_to_ch = data_c[0].split(' ')										# get data from the packet
		print data_to_ch[1]
		if accept == data_to_ch[1]:												# check against the codes for accept or error
			print "File received from the server.."
			new_bit_file = "\n".join(data_back[7:])
			file_cl = filename.split('/')
			file_n = 'new_'+file_cl[-1]
			f = open(file_n, 'wb')
			f.write(new_bit_file)												# save new file with data transferred.
			print "file downloaded from the server.."
			print "Connection closed from the server.."
		elif error == data_to_ch[1]:
			print "404 error recovered.."
			print "File not found in the server.."	
			print "Connection closed from the server.."
			
	s.close()																	# close connection from the client side.

if __name__ == '__main__':
	Main(sys.argv[1],sys.argv[2],sys.argv[3])
			
