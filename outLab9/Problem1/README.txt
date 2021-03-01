
peer.cpp: -	It is a menu driven program for peers which can publish the files to central server which
	 	it wants to share to other peers & and it can search for files through central server get
	 	that file from respective peer.
	 	
	 	IMP FUNCTIONS
	 	startPServer() - It will start the server for peer in background to serve incoming request
	 	of fellow peers
	 	connToServer() - It will establish a connection with central server
	 	displayMenu()  - It is used to display Menu for intraction
	 	
server.cpp: -	It is a program for central server which will establish a server for all the peers to connect
		and fetch iformation about others.
		
		IMP FUNCTIONS
		startServer() - It is used to start and initialise the server
		acceptPeer()  - Accepts incoming peers request & stores its information 		 
		
peerinfo.hpp: -	It conatins a user defined class which stores all the necessary detials of peer who has 
		established connectiom with server  
	
