OBJECTS=main.o hello.o factorial.o

hello: $(OBJECTS)
	$(CXX) $(OBJECTS) -o hello
main.o: main.cpp functions.h
	$(CXX) -c main.cpp
hello.o: hello.cpp functions.h
	$(CXX) -c hello.cpp
factorial.o: $(FACTM)
	$(CXX) -c factorial.cpp
	
clean:
	rm -rf *.o hello
