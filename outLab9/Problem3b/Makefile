hellomake: hellomake.o hellofunc.o
	gcc $^ -o $@
hellomake.o: hellomake.c hellomake.h
	gcc -c $<
hellofunc.o: hellofunc.c hellomake.h
	gcc -c $<
	
clean:
	rm -rf *.o hellomake
