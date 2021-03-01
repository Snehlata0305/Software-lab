#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <string>
#include <unistd.h>
#include <arpa/inet.h>
#include <fcntl.h>

#define S_PORT 4500 											// Fixed port no. for SERVER
#define BUFFER_SIZE 1024

using namespace std;

int startPServer(int pport, int &psoc);							// To start peers background server
int connToServer(int &psocket, string serIP, int port);			// Establish connection with diffferent server
int checkNdie(int status);										// Check for return values of varous function
int displayMenu();
int mySend(int sSoc, string &input);
char buffer[BUFFER_SIZE];										// Buffer to store sent & recieved data

int main(int argc, char const *argv[])
{
	int stat;													// Temp variable used to store return value of functions
	int peersocket;												// Socket in which peers server is listening
	int p2sSocket;												// Socket for communication with central server
	int fileDes;												//	Descriptor for file
	string file_name;
	string op;

	if( argc != 4)
	{
		cout<<"Run as: ./peer <Server Port> <Server IP> <Peer Port>\n";
		return 1;
	}
	
	startPServer(atoi(argv[3]), peersocket);

	cout<<"Connecting to Central server...\n";
	connToServer(p2sSocket, argv[2], atoi(argv[1]));					// Connects to central server
	snprintf(buffer, BUFFER_SIZE, "%s", argv[3]);					// Sends peer's server port no. to central server  
	send(p2sSocket, buffer, BUFFER_SIZE, 0);

	int process = fork();
		if( process > 0)
		{	
			do
			{
				displayMenu();
				mySend(p2sSocket, op);

					if( !strncmp(op.c_str(), "1", 1) )
					{	
						cout<<"Publish File : ";
						mySend(p2sSocket, file_name);						// Publishes the file names to server
						perror("Publish");
					}	
					else if( !strncmp(op.c_str(), "2", 1) )
					{	
						cout<<"Search File : ";
						mySend(p2sSocket, file_name);

						recv(p2sSocket, buffer, BUFFER_SIZE, 0);
							if( strncmp(buffer, "NF", 2) )
							{
								string p2pIP = string(buffer);
								cout<<"File is at: "<<p2pIP;
								recv(p2sSocket, buffer, BUFFER_SIZE, 0);
								string p2pPORT = string(buffer);
								cout<<"::"<<p2pPORT<<"\n";

								int p2pSocket;
								cout<<"Connecting to peer : "<<p2pIP<<":"<<p2pPORT<<"\n";
								connToServer(p2pSocket, p2pIP, atoi(p2pPORT.c_str()));		// Connects to other peer for download
								cout<<"Connection Established...\n";

								snprintf(buffer, BUFFER_SIZE, "%s", file_name.c_str());
								send(p2pSocket, buffer, BUFFER_SIZE, 0);

								snprintf(buffer, BUFFER_SIZE, "p2p-files/%s", file_name.c_str());
								fileDes = open(buffer, O_RDWR | O_CREAT | O_APPEND );		// Open the file to write
								perror("File open");

								int Bsize;
								int fsize=0;

								cout<<"Downloading "<<file_name<<" ...\n";
									while( (Bsize = read(p2pSocket, buffer, BUFFER_SIZE)) > 0 )			// Read from peer & write in file
									{
										fsize += Bsize;
										//perror("Read");
										write(fileDes, buffer, Bsize);
									}

								cout<<"Size = "<<fsize;
								close(fileDes);
								cout<<" Downloaded successfully "<<"\n";
								close(p2pSocket);
							}
							else
								cout<<"File not Found\n";
					}	
			}while( strncmp(op.c_str(), "3", 1) );
		}
		else
		{
			while(1)
			{
				struct sockaddr_in in_peer;								// For storing incoming peers address
				socklen_t addrlen;
				int in_peerFD;
				char data[BUFFER_SIZE];

				addrlen 	= 	sizeof(in_peer);
				in_peerFD 	= 	accept(peersocket, (struct sockaddr *)&in_peer, &addrlen);

				recv(in_peerFD, buffer, BUFFER_SIZE, 0);
				snprintf(data, BUFFER_SIZE, "p2p-files/%s", buffer);
				fileDes = open(data, O_RDONLY);							// Open File From Where to read
				// perror("File open");
				int Bsize;

					while( (Bsize = read(fileDes, buffer, BUFFER_SIZE)) > 0 )
					{
						write(in_peerFD, buffer, Bsize);
					}
				close(fileDes);
				close(in_peerFD);
			}
		}

	close(peersocket);
	close(p2sSocket);
	return 0;
}

int startPServer(int pport, int &psoc)
{
	cout<<"Starting peer's server...\n";
	struct sockaddr_in peer_server;
	int stat	=	-1;			// Temp variable used to store return value of functions
	
	psoc = socket(AF_INET, SOCK_STREAM, 0);
		/* Checks for succesfull creation of socket */ 
	perror("Peer's Socket");
	checkNdie(psoc);
	
	bzero(&peer_server, sizeof(peer_server));
	peer_server.sin_family			=	AF_INET;
	peer_server.sin_addr.s_addr 	=	htonl(INADDR_ANY);
	peer_server.sin_port			=	htons(pport);

	int optval = 1;
    setsockopt(psoc, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));
	stat	=	bind(psoc, (struct sockaddr *)&peer_server, sizeof(peer_server));	
			/* Checks for binding of port & address */
	perror("Bind");
	checkNdie(stat);

	stat	=	listen(psoc, 5);
		/* Checks for listen error */
	perror("Listen");
	checkNdie(stat);
	return 0;
}

int mySend(int sSoc, string &input)
{
	getline(cin, input);
	snprintf(buffer, BUFFER_SIZE, "%s", input.c_str());
	send(sSoc, buffer, BUFFER_SIZE, 0);
	return 0;
}

int connToServer(int &psocket, string serIP, int port)
{
	int stat;
	struct sockaddr_in cen_server;
	char serip[50];
	strcpy(serip, serIP.c_str());

	psocket = socket(AF_INET, SOCK_STREAM, 0);
	/* Checks for succesfull creation of socket */ 
	perror("Socket");
	checkNdie(psocket);

	cen_server.sin_family		=	AF_INET;
	cen_server.sin_addr.s_addr 	=	inet_addr(serip);
	cen_server.sin_port			=	htons(port);

	stat	=	connect(psocket, (struct sockaddr *)&cen_server, sizeof(cen_server));
	/* Checks For successfull connection */
	perror("Connect");
	checkNdie(stat);
}

int displayMenu()
{
	cout<<"\n******Peer Main Menu******";
	cout<<"\n\t1. Publish";
	cout<<"\n\t2. Search & Fetch";
	cout<<"\n\t3. Exit";
	cout<<"\nSelect an option : ";
	return 0;
}

int checkNdie(int status)
{
	if( status < 0 )
		exit(1);

	return 0;
}