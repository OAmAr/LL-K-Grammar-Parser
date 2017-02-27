def buildFirstsets(self):
	self.firstsets={}
	for rule in self.gram.getRules():
		self.firstsets[rule.getVal()]=self.firstSet(rule.getVal()) #each variable gets the set it creates
	#terminals get their set returned and also added to firstsets in the thingy

def firstSet(self, symbol):
	if symbol in self.firstsets: 
	#if we've already computed it, just return it
		return self.firstsets[symbol]
	if symbol not in self._non_terms: 
	#if its a non terminal. rule 0 is given, first set is just symbol
		self.firstsets[symbol] = dict(symbol:set([False])
		return self.firstsets[symbol]
	
	_range = self.gram.getRule(symbol)
	#this is the range of rules in our grammar that come from symbol
	_range[0]+=1
	_range[1]+=1 #because i indexed rules it stupidly

	#So what we need to do now is, we have the empty dict firstS
	firstS = dict()
	#we want to populate it with each symbol in the first set for symbol, and the rule that we're on when we find it
	
	for rule_i in _range:
		rule = self.gram[rule_i]
		#rule_i is what we put in set
		yld = self.gram.getYield[0]
		for key in self.followSet(yld[0]):
		#this returns the dict full of keys and rules in self.followSet
			if key not in firstS: #if the set already exists init
				firstS[key]=set()
			first[key].add(rule_i)
	return firstS #test this, i think it works 
