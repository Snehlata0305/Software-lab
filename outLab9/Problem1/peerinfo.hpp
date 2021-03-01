#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

class peerInfo
{
	private:
		int socID;										// Socket in which peer is communicating with server
		int port;										// Port in which peer's server is running
		string IP;										// IP address of Peer
		vector<string> files;							// List of File peers have

	public:
		peerInfo(int socketFD, string ip, int p)
		{
			socID	=	socketFD;
			IP 		=	ip;
			port 	=	p;
		}

		string getIP(){return IP;}

		int getPort(){return port;}

		int getsocID(){return socID;}

		string getFile(int index){return files[index];}

		void addFile(string file)									// Add new file to the list
		{
			files.push_back(file);
		}

		int searchFile(string sFile)								// Search for particular file in peers list of files
		{
			for (int i = 0; i < files.size(); ++i)
				if ( files[i] == sFile )
					return 1;

			return 0;
		}
};