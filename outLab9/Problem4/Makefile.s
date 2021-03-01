SERVPATH=./mt_server/
TLPATH= $(path)
HDEP=sv_task.h sv_utils.h
CFLAGS=-c -g -pthread -Wextra
OBJECT = build
PATH_TO_EXEC = $(path)/server.out

all: $(OBJECT) server
$(OBJECT):
	if [ ! -d ./$(OBJECT) ];then \
		mkdir -p $(OBJECT);   \
	fi

server: $(TLPATH)/server.out
$(TLPATH)/server.out: $(OBJECT)/mt_server.o $(OBJECT)/sv_task.o $(OBJECT)/sv_utils.o
	$(CC) -pthread $^ -o $@
$(OBJECT)/mt_server.o: mt_server.c $(HDEP)
	$(CC) $(CFLAGS) $< -o $@
$(OBJECT)/sv_task.o: sv_task.c $(HDEP)
	$(CC) $(CFLAGS) $< -o $@
$(OBJECT)/sv_utils.o: sv_utils.c sv_utils.h
	$(CC) $(CFLAGS) $< -o $@
	
run:
	$(PATH_TO_EXEC) $(port)
clean:
	@rm -rf $(OBJECT)/*.o $(PATH_TO_EXEC) $(OBJECT)
