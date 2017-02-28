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


#	def populateParsetable(self):
#		self.resetParsetable()
#		#print("")
#		#print("Firstsets: ", self.firstsets)
#		#print("Followsets: ", self.followsets)
#		keys_considered = set()	
#		if True:
#			return
#		#	for term in ##iterate through keys in self.first, check if null, if null add follow set and go on 
#
#		for rule_i in range(1, self.gram.getLength()+1):
#			print("Considering rule: ", rule_i, self.gram[rule_i])
#			key = self.gram[rule_i].getVar()
#			if key not in keys_considered:
#				keys_considered.add(key)
#				for term in self.firstsets[key]:
#					if term == "/":
#						for _term in self.followsets[key]:
#							self.parsetable[_term][key].add(rule_i) #how to get the index of rule which empty sting comes from
#					else:
#						self.parsetable[term][key].add(rule_i)
#

	def populateParsetable(self):
		self.resetParsetable()
		print("")
		print("First sets: " , self.firstsets)
		print("Followsets: " , self.followsets)
		keys_considered= set()
		for non_term in self._non_terms:
			return

	def buildFollowsets(self):
		self.followsets = {}
		for rule in self.gram.getRules():
			self.followsets[rule.getVar()]= set()
		nextset = self.followset('S')
		while nextset != self.followsets:
			self.followsets = nextset
			nextset = self.followset('S')

	def oldfollowset(self, symbol):
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
	

	def followset(self, symbol):
		nextset = deepcopy(self.followsets)
		if symbol == "S":
			nextset['S'].add('$')
		for rule_i in range(1,self.gram.getLength()+1):
			rule = self.gram[rule_i]
			yld = rule.getYield()[0]
			for i in range(len(yld)):
				char = yld[i]
				if char in self._non_terms:
					if i+1 == len(yld) and char!=rule.getVar():
						nextset[char] = nextset[char] | nextset[rule.getVar()]
						break
					else:
						remove = yld[i+1] in self.firstsets
						if "/" in self.firstSet(yld[i+1]):
							nextset[char] = nextset[char] | nextset[rule.getVar()]
						nextset[char] = nextset[char] | set(self.firstSet(yld[i+1])) - set(['/'])
						if remove:
							del self.firstsets[yld[i+1]]
			return nextset




	def buildFirstsets(self): #builds the greater set of followsets
		self.firstsets={}
		for rule in self.gram.getRules():
			self.firstsets[rule.getVar()] = self.firstSet(rule.getVar())
		#print(self.firstsets)
	
	
	def firstSet(self, symbol):
		#print("Called on ", symbol)
		if symbol in self.firstsets: #base case 1
			return self.firstsets[symbol]
		if symbol not in self._non_terms: #base case 2
			 self.firstsets[symbol] = {symbol:set([False])} #dont come from a rule, just symbol
			 return self.firstsets[symbol]


		_range = self.gram.getRuleRange(symbol) #get range as a set of integers where rule starts with symbol
		
		firstS=dict() #empty dictionary
		#print("")
		#print(symbol,_range)
		for rule_i in range(_range[0],_range[1]):
			rule = self.gram[rule_i]
		#	print("Considering: ", rule)
			yld  = rule.getYield()[0]
			for key in self.firstSet(yld[0]):
		#		print("Adding " , key, "to", symbol)
				if key not in firstS:
					firstS[key]=set()
				firstS[key].add(rule_i)

		return firstS

	

