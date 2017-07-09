'''
... author :: 'Saathvik Prasad'...
	
   ....... The program is modified and the base idea of the program was adopted from the project skeleton provided........

 * This is the program for multithreaded server part of the 'Mutithreaded server client system'.
 * The program uses the HTTP packet format to handle the request from the client.
 * The program defines a user file retrival function to handle the file retrival and responce to the client. The file name is retrieved from the 
 	client request packet and the file is checked in the system. The file name can be given as a 'name of file' or the exact 'path to the file'.
 * The file is searched in the system using the os.path library, and the associated informationn from the system about the file is also retrieved
 	to inform the user and pass them the information.
 * The program then returns the file contents to the client through a HTTP responce packet.
 * If the file is not found in the system, then a '404' error is sent back and displayed in the browser. 
 * The system uses 2 HTTP codes to respond to the client when it requires for a file
 	codes are:: correct == 200;; file found in the system, associated information encapsulated in the responce packet.
 				wrong == 404;; file not found in the system, check path of file or name of the file. Contains no information about the file.
 * The function is then run in a multithreaded environment and when each new connection is accepted, a new thread is started to run the above program to serve 
 	each clients individually.
 * Apart from the file retrival function, the system is supported with 2 other utility functions to create a responce packet for the correct and error messages.
 * The system prints the messages(log) to terminal.

 * The program is written in python 2.7+ version using Linux mint. The required libraries have been imported in the program.

'''


import socket
import threading
import os
import datetime
import webbrowser
import sys


'''
Utility function to create a new responce packet for file found in the system message
'''
def prepare_ok_pkt(code,fsize,mtime):
	print "Preparing responce packet.."
	head1 = "HTTP/1.1 "+str(code)+" "+"OK"
	head2 = "Connection:close"
	time_of_pkt = datetime.datetime.now()
	head3 = "Date: "+str(time_of_pkt)															# date and time of packet created.
	head4 = "Server: Linux Mint"
	head5 = "Last Modified time: "+str(mtime)													# modified time of the file
	head6 = "Length: "+str(fsize)																# length of the file	
	head7 = "Content Type: text/html"
	final_head_pkt = head1+"\n"+head2+"\n"+head3+"\n"+head4+"\n"+head5+"\n"+head6+"\n"+head7	# append all the header info to one header string
	return final_head_pkt																		# return the created header


'''
Utility function to create a new responce packet for file not found in the system message
'''
def prepare_err_pkt(code):
	print "Preparing responce packet.."
	head1 = "HTTP/1.1 "+str(code)+" "+"Error"
	head2 = "Connection:Close"
	final_err_pack = head1+"\n"+head2
	return final_err_pack																		# return the created header


'''
Function to handle the file requests from the client
The function includes the functionalities like::
--receive packet form the client
--search for file 
--get file details
--prepare responce packet
--send back the packet to the client
'''
def userfile_retr(name, sock):

	req_from_client = sock.recv(2048)															# get data from the client
	print "data is: "+str(req_from_client)
	filename = req_from_client.split()
	file_to_search = str(filename[1])
	print "filename requested by client with or without path is.." +str(file_to_search[1:])		# print log message.
	if os.path.isfile(file_to_search[1:]):														#check if file exists in the system.
		http_code = 200																			# prepare 'ok' packet with code 200
		size_f = os.path.getsize(file_to_search[1:])											# get file details from the system
		last_modify_time = os.path.getmtime(file_to_search[1:])
		resp_packet = prepare_ok_pkt(http_code,size_f,last_modify_time)							# get header packet
		with open(file_to_search[1:], 'rb') as f:												# open file to read contents
			file_bytes = f.read(2048)															# create a new string with file contents
		final_resp_packet = resp_packet+"\n"+file_bytes											# append the file to the responce body (chapter 2 packet format)
		print "Sending responce to the client.."
		sock.send(final_resp_packet)															# send packet back to the client
		print "Launching file for client.."
		print "Closing connection to the client.."
		webbrowser.open('file://'+ os.path.abspath(file_to_search[1:]))							# open the file
	else:
		print "File not found in the system..404.."										
		err_pack = prepare_err_pkt(404)															# prepare 'error' packet with code 404
		print "Sending responce to the client.."
		sock.send(err_pack)																		# send packet back to the client
		webbrowser.open('file://'+ os.path.abspath('err.html')									# display error page
		print "Closing connection to the client.."

	
	sock.close()																				# close connection to the client after serving the file request


'''
Main function used to define the ip address and port number for the server accept the connection from the client
'''
def Main():
	host = sys.argv[1]																			# set ip address for the server
	port = int(sys.argv[2])																		# set port number for the server
	
	s = socket.socket()																			# create a new socket
	s.bind((host,port))																			# bind the host and the port

	s.listen(5)																					# listen for the connection request from the client
	
	print "Server Running..."
	print "Server Waiting for connection..."

	while True:																					# keep server running
		conn,address = s.accept()																# accept the connection from a client
		print "Connection accepted from.." +str(address)
		
		th = threading.Thread(target = userfile_retr, args=("New Connection",conn))				# create a new thread for the client to retrieve the file
		print "New Thread created for the new client connection"
		th.start()																				# start the tread
	s.close()																					# close connection when closed manually

if __name__ == '__main__':
	Main()
		
