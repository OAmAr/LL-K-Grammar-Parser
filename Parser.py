import Grammar
from copy import deepcopy
class Parser:
	def __init__(self,):
		self.gram = None
		self.look_ahead = 1
		self.stack = ["$"]			#list stack, append pushes, 
		self._non_terms=set()
		self._terms = set("$")
		self.parsetable = self.resetParsetable() #dict of {non_term:{term:(first,follow)}
		self.firstsets={}
		self.followsets={}

	def setGrammar(self, gram):
		self.gram = gram
		self.setNonTerms()
		self.setTerms()
		self.stack = ['$', 'S']
		self.buildFirstsets()
		self.buildFollowsets()
		self.populateParsetable()
	
	def setLook_ahead(self, k):
		self.look_ahead = 1
		print("Look ahead currently limited to 1")
	
	def describe(self):
		print("\nThis is a LL(%d) shift reducing grammar parser" % (self.look_ahead))
		if self.gram == None:
			print("No grammar set")
			return
		print("It is using the following grammar: ")
		print(self.gram)
		self.describeParse()
		self.describeStack()
	
	def describeParse(self):
		return		

	def describeStack(self):
		print("Current Stack:")
		print("bottom ", self.stack, " top")

	def setNonTerms(self):
		self._non_terms = set()
		for rule in self.gram.getRules():
			self._non_terms.add(rule.getVar())
	
	def setTerms(self):
		self._terms = set('$')
		for rule in self.gram.getRules():
			for yld in rule.getYield():
				self._terms= self._terms | set(char for char in yld)
		self._terms = self._terms - self._non_terms - set("/")

	
	def resetParsetable(self):
		inner = dict(zip(self._non_terms, [set().copy() for i in range(len(self._non_terms))]))
		inn_cop = [deepcopy(inner) for i in range(len(self._terms))]
		self.parsetable = dict(zip(self._terms, inn_cop))
		#dict of {term:{non_term:(rule_number)}

	def oldpopulateParsetable(self):
		self.resetParsetable()
		
		for i in range (1,self.gram.getLength()+1):
			term = self.gram[i].getYield()[0][0] 
			#this ugly string gives the ith rule, which will always be a singleton, gets its yield, a list with 1 value, gets its only value and gets its first character
			if term  == "/":
				continue
					
			while term in self._non_terms: #if first var, recursively look a terminal
				for j in range(1,self.gram.getLength()+1):
					if self.gram[j].getVar() == term:
						term = self.gram[j].getYield()[0][0]
						break
					#else:
					#	print("Something went wrong") 
					#	break
		
			self.parsetable[term][self.gram[i].getVar()].add(i)
		return

	def populateParsetable(self):
		self.resetParsetable()
		print("")
		print("Firstsets: ", self.firstsets)
		print("Followsets: ", self.followsets)
		keys_considered = set()	

		for rule_i in range(1, self.gram.getLength()+1):
			rule = selfgram[rule_i]
			key = rule.getYields()[0][0]
			for term in ##iterate through keys in self.first, check if null, if null add follow set and go on 

		for rule_i in range(1, self.gram.getLength()+1):
			print("Considering rule: ", rule_i, self.gram[rule_i])
			key = self.gram[rule_i].getVar()
			if key not in keys_considered:
				keys_considered.add(key)
				for term in self.firstsets[key]:
					if term == "/":
						for _term in self.followsets[key]:
							self.parsetable[_term][key].add(rule_i) #how to get the index of rule which empty sting comes from
					else:
						self.parsetable[term][key].add(rule_i)
					
		#for key in self._non_terms:
		#	for term in self.firstsets[key]:
		#		if term == "/":
		#			for _term in self.followsets[key]:
		#				self.parsetable[_term][key].add(key) #how to get the rule from the non_term
		#		else:
		#			self.parsetable[term][key].add(key)
		
		
		#for rule_i in range(1, self.gram.getLength()):
		#	rule = self.gram[rule_i]
		#	yld = rule.getYield()[0]
		#	for term in self.firstsets[yld[0]]:
		#		if term != '/':
		#			self.parsetable[term][rule.getVar()].add(rule_i)
		#		else:
		#			for _term in self.followsets[rule.getVar()]:
		#				self.parsetable[_term][rule.getVar()].add(rule_i)
		
		
	def resetstack(self):
		self.stack = ['$', 'S']

	#this is only LL[1] right now, must be unambiguous, non recursive
	
	def parse(self, string):
		#self.preparse()	
		print("")
		print("Firstsets: ", self.firstsets)
		print("Followsets: ", self.followsets)
		print("Parsetable: ", self.parsetable)
		string+="$"
		self.resetstack()
		stack = self.stack
		ops = []
		i=0

		while i <= len(string):
			if stack == []:
				return True
			char=string[i]
			print("Considering: ", char)
			if char == stack[-1]:
				stack.pop()
				i+=1

			else:
				try:
					rule_i = list(self.parsetable[char][stack.pop()])[0]
				except IndexError:
					print("Rejected")
					return False
				ops.append(rule_i)
				for t in self.gram[rule_i].getYield()[0][::-1]:
					stack.append(t)
			self.describeStack()
				
		if stack == []:
			return True
		else:
			return False
	
	def buildFirstsets(self):
		self.firstsets={}
		for rule in self.gram.getRules():
			self.firstSet(rule.getVar())
		#print(self.firstsets)
			

	def firstSet(self, symbol):
		if symbol in self.firstsets:
			return self.firstsets[symbol]
		if symbol not in self._non_terms:
			self.firstsets[symbol] = dict(symbol:set([0])) 
			return self.firstsets[symbol]

		firstS = dict()
		rule = self.gram.getRule(symbol)
		if rule == False:
			print("Error, no rule: ", symbol)			
			raise(RuntimeError)
		_range = self.gram.getRuleRange(symbol)
		_range[0]+=1
		_range[1]+=1

		for sub_rule_i in _range:
			sub = self.gram[sub_rule_i]
			term = sub.getYield()[0][0]
			rec = self.firstSet(term) #this is dict of 
			firstS[sub.getVar()] = self.firstset[sub.getVar()][sub.getYield

		for sub in self.gram.getRule(symbol).getYield():
			firstS= firstS | self.firstSet(sub[0])
		
		self.firstsets[symbol]=firstS
		return firstS	

	def buildFollowsets(self):
		self.followsets={}
		
		for rule in self.gram.getRules():
			self.followsets[rule.getVar()] = set() #maybe make it a tuple of which rule comes from which?
		
		nextset=self.followset('S')
		
		while nextset != self.followsets:
			self.followsets=nextset
			nextset = self.followset('S')
				


	def followset(self, symbol):
		nextset=deepcopy(self.followsets)
		if symbol == "S":
			nextset['S'].add('$') #start symbol always followed by $
		
		for rule_i in range(1,self.gram.getLength()+1):
			rule = self.gram[rule_i]
			yld = rule.getYield()[0]
			for i in range(len(yld)):
				char = yld[i]
				if char in self._non_terms:
					#apply rules:
					if i+1 == len(yld) and char!= rule.getVar():
						#add follow of lhs
						nextset[char] = nextset[char] | nextset[rule.getVar()]
						break #break because nothing else next to it
					elif "/" in self.firstsets[yld[i+1]]:
						#if nextstring can be empty, add its follow
						nextset[char] = nextset[char] | nextset[rule.getVar()]
					#always add first of next string to follow
					nextset[char] = nextset[char] | (self.firstSet(yld[i+1]) - set(['/']))
		return nextset
						
					
					
	
	
	
	
	
	
	
	
	
	
	def oldfollowset(self, symbol):
		if self.followsets[symbol] != set():
			return self.followsets[symbol] #already computed
		
		if symbol == "S":
			self.followsets['S'].add("$") #start symbol always gets
		
		for rule in self.gram.getRules(): #for each subrule
			print(rule)
			for sub in rule.getYield():
				for i in range(len(sub)): #check each character
					if sub[i] in self._non_terms: #if its a nonterminal
						if i+1 == len(sub) or "/" in self.firstsets[sub[i+1]]: #if its at the end of the rule and not its own rule, it gets the follow of the rule
							if rule.getVar() != sub[i]: #dont want recurse
								self.followsets[sub[i]] | self.followset(rule.getVar()) #rule 2, if end of production, folowed by follow of lhs
						
							if i+1 == len(sub):
								break #if we're at end of the rule just break instead of doing next tests
						self.followsets[sub[i]] | self.firstsets[sub[i+1]]
