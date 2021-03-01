CLPATH= ./mt_client/
TLPATH= $(path)
HDEP=cl_task.h cl_utils.h
CFLAGS=-c -g -pthread -Wall
OBJECT = build

NUM_THREADS = 10
HOST_NAME = localhost
PATH_TO_EXEC = $(path)/client.out

all: $(OBJECT) client
$(OBJECT):
	if [ ! -d ./$(OBJECT) ];then \
		mkdir -p $(OBJECT);   \
	fi
client: $(TLPATH)/client.out

$(TLPATH)/client.out: $(OBJECT)/mt_client.o $(OBJECT)/cl_task.o $(OBJECT)/cl_utils.o
	$(CC) -pthread $^ -o $@
$(OBJECT)/mt_client.o: mt_client.c $(HDEP)
	$(CC) $(CFLAGS) $< -o $@
$(OBJECT)/cl_task.o: cl_task.c $(HDEP)
	$(CC) $(CFLAGS) $< -o $@
$(OBJECT)/cl_utils.o: cl_utils.c cl_utils.h
	$(CC) $(CFLAGS) $< -o $@
	
run:
	$(PATH_TO_EXEC) $(HOST_NAME) $(port) $(NUM_THREADS)



	
clean:
	@rm -r $(PATH_TO_EXEC) $(OBJECT)/*.o $(OBJECT)
