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


	def populateParsetable(self):
		self.resetParsetable()
		print("")
		print("Firstsets: ", self.firstsets)
		print("Followsets: ", self.followsets)
		keys_considered = set()	
		if True:
			return
		#	for term in ##iterate through keys in self.first, check if null, if null add follow set and go on 

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
