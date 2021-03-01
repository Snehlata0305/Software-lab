class BlackMoneyHolder:
    ## write your code here
    def __init__(self,name,accounts_info):
    	self.name=name
    	self.accounts_info=accounts_info
    	if(type(self.name)!=str or self.name=="" or self.name==None):
    		raise Exception('Name not String or is None or is empty')
    	if(type(self.accounts_info)!=dict):
    		raise Exception('Accounts_info not Dictionary')
    		
    	self.newlist = sorted (self.accounts_info.items())
    			
    def update_amount(self, bnkname, bnkamt):
    	self.accounts_info.update({bnkname:bnkamt})
    	
    def total_black_money(self):
    	totamt = 0;
    	for v in self.accounts_info.values():
    		totamt+=v
    	return totamt

    def __lt__(self,other):
    	return self.total_black_money() < other.total_black_money()
    
    def __eq__(self,other):
    	return self.total_black_money() == other.total_black_money()
    	
    def __gt__(self,other):
    	return self.total_black_money() > other.total_black_money()
    	
        	
    def __str__(self):
    	strop = ""
    	for y in sorted(self.accounts_info):
    		strop = strop + y +': '+ str(self.accounts_info[y]) +"\n"
    	return strop
    	
    def __len__(self):
    	return len(self.accounts_info)
    	
    def __getitem__(self, index):
    	self.newlist = sorted (self.accounts_info.items())
    	z = tuple(self.newlist[index])
    	return z
