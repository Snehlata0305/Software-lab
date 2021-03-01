SUBDIRS = mt_client mt_server
SERVER= ./mt_server
CLIENT= ./mt_client
path = $(shell pwd)
port = 8080 
export path port 
.PHONY: all clean run_server run_client

all clean:
	for dir in $(SUBDIRS); do\
		$(MAKE) -C $$dir -f Makefile $@; \
	done
run_server:
	
	$(MAKE) -C $(SERVER) run
run_client:
	
	$(MAKE) -C $(CLIENT) run
# server:
# 	$(MAKE) -C $(SERVER)
# client:
# 	$(MAKE) -C $(CLIENT)
# clean: $(CLEAN_SERV) $(CLEAN_CL)
# $(CLEAN_SERV):
# 	$(MAKE) -C $(SERVER) clean
# $(CLEAN_CL):
# 	$(MAKE) -C $(CLIENT) clean