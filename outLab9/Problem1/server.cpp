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
#include "peerinfo.hpp"

#define S_PORT 4500 						// Fixed port no. for SERVER
#define BUFFER_SIZE 1024

using namespace std;

int startServer(int &serverSocket, int sPort);			// Function used to Initialise and start the server
int acceptPeer(int soc);					// Accept new connection and returns FD for that client
int checkNdie(int status);					// Check for return values of varous function 
vector<peerInfo> peers;						// Saves the Informations of all peers which are connected
char buffer[BUFFER_SIZE];
char data[BUFFER_SIZE];

int main(int argc, char const *argv[])
{
	fd_set masterFDS;
	fd_set readFDS;

	int serverSocket=0;
	int maxFD;
	int stat;								// Temp variable used to store return value of functions

	if( argc != 2)
	{
		cout<<"Run as: ./server <Server Port>\n";
		return 1;
	}

	startServer(serverSocket, atoi(argv[1]));
	cout<<"Server Socket : "<<serverSocket<<"\n";

	FD_ZERO(&masterFDS);
	FD_ZERO(&readFDS);
	FD_SET(serverSocket,&masterFDS);
	maxFD	=	serverSocket;

		while(1)
		{
			fflush(stdout);
			readFDS	=	masterFDS;
			stat 	=	select(maxFD+1, &readFDS, NULL, NULL, NULL);
			checkNdie(stat);

				for (int i = 0; i <= maxFD; ++i)				// Itterate through every fd to check activity
				{
					if ( FD_ISSET(i, &readFDS) )
					{
						if ( i == serverSocket)					// For new connection if activity is in server's socket
						{
							int peerFD	=	acceptPeer(serverSocket);		// Accept new Peer connection  
							if( peerFD > 0)											// only if valid FD is returned
							{
								FD_SET(peerFD, &masterFDS);
									if ( peerFD > maxFD )
									{
										maxFD	=	peerFD;
									}
							}
						}
						else									// Handles incoming data from peers
						{
							recv(i, data, BUFFER_SIZE, 0);

							if( !strncmp(data, "1", 1) )				// IF peer want to publish, add file in peer's info
							{
								recv(i, buffer, BUFFER_SIZE, 0);
									for (int j = 0; j < peers.size(); j++)
									{
										if ( peers[j].getsocID() == i)
										{
											peers[j].addFile(buffer);
										}
									}
							}
							else if( !strncmp(data, "2", 1) )				// IF peer wants to search for a file
							{
								recv(i, buffer, BUFFER_SIZE, 0);
								int found = 0;
									for (int j = 0; j < peers.size(); j++)
									{
										if( peers[j].searchFile( string(buffer) ))
										{
											found = 1;
											snprintf(buffer, BUFFER_SIZE, "%s", peers[j].getIP().c_str());
											send(i, buffer, BUFFER_SIZE, 0);
											snprintf(buffer, BUFFER_SIZE, "%d", peers[j].getPort());
											send(i, buffer, BUFFER_SIZE, 0);
											break;
										}
									}	
									if ( !found )
									{
										snprintf(buffer, BUFFER_SIZE, "NF");
										send(i, buffer, BUFFER_SIZE, 0);
									}
							}
							else if( !strncmp(data, "3", 1) )				// Show all files of that user
							{
									for (int j = 0; j < peers.size(); j++)
									{
										if ( peers[j].getsocID() == i)
										{
											cout<<"Peer Disconnected : "<<peers[j].getIP()<<"::"<<peers[j].getPort();
											cout<<" socket : "<<peers[j].getsocID()<<"\n";
											peers.erase( peers.begin()+j );
											close(i);
											FD_CLR(i, &masterFDS);
										}
									}	
							}							
							// else if( !strncmp(data, "0", 1) )				// Show all files of that user
							// {
							// 		for (int j = 0; j < peers.size(); j++)
							// 		{
							// 			if ( peers[j].getsocID() == i)
							// 			{
							// 				cout<<"Files of "<<peers[j].getIP()<<"::"<<peers[j].getPort()<<"\n";
							// 				peers[j].showFiles();
							// 			}
							// 		}	
							// }
						}
					}
				}
		}

	close(serverSocket);

	return 0;
}

int startServer(int &serverSocket, int sPort)
{
	int stat			=	-1;			// Temp variable used to store return value of functions
	int serverPort		=	sPort;
	struct sockaddr_in cen_server;
	int i 	=	0;

	serverSocket = socket(AF_INET, SOCK_STREAM, 0);
		/* Checks for succesfull creation of socket */ 
	perror("Socket");
	checkNdie(serverSocket);
	
	bzero(&cen_server, sizeof(cen_server));
	cen_server.sin_family		=	AF_INET;
	cen_server.sin_addr.s_addr 	=	htonl(INADDR_ANY);
	cen_server.sin_port			=	htons(serverPort);

	int optval = 1;
    setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));
	stat	=	bind(serverSocket, (struct sockaddr *)&cen_server, sizeof(cen_server));	
			/* Checks for binding of port & address */
	perror("Bind");
	checkNdie(stat);

	stat	=	listen(serverSocket, 5);
		/* Checks for listen error */
	perror("Listen");
	checkNdie(stat);
	return 0;
}

int acceptPeer(int soc)
{
	struct sockaddr_in peer;
	socklen_t addrlen;
	int peerFD;

	addrlen	=	sizeof(peer);
	peerFD	=	accept(soc, (struct sockaddr *)&peer, &addrlen);
		if( peerFD == -1 )
			perror("Accept");
		else
		{
			recv(peerFD, buffer, BUFFER_SIZE, 0);				// Recieves port no. from peer in which it is working
								
			/* Add peer's info in vector of all peers */
			peers.push_back(peerInfo(peerFD, inet_ntoa(peer.sin_addr), atoi(buffer)));
			cout<<"New peer connected : "<<inet_ntoa(peer.sin_addr)<<"::"<<buffer<<" socket : "<<peerFD<<"\n";
		}

	return peerFD;
}

int checkNdie(int status)
{
	if( status < 0 )
		exit(1);

	return 0;
}