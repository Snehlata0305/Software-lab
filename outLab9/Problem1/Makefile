.PHONY: all peer server
all: peer server
peer: peer.cpp
	g++ peer.cpp -o peer
server: server.o
	g++ server.o -o server
server.o: server.cpp peerinfo.hpp
	g++ -c server.cpp
	
clean:
	rm -rf *.o peer server
