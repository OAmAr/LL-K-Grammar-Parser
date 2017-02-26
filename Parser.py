import Grammar

class Parser:
	def __init__(self, gram):
		self.gram = None
		self.look_ahead = 1
		self.parsetable=dict(dict()) #dict of {term:{non_term:(first,follow)}
		self.stack = ["$"]			#list stack, append pushes, 

		self._non_terms=set()
		self._terms = set()
	
	def setGrammar(self, gram):
		self.gram = gram
		self.setNonTerms()
		self.setTerms()
		self.setParseTable()
	
	def setLook_ahead(self, k):
		self.look_ahead = 1
	
	def describe(self):
		print("This is a LL(%k) shift reducing grammar parser" % (self.look_ahead))
		print("It is using the following grammar: ")
		print(self.gram)
		self.describeParse()
		self.describeStack()
	
	def describeStack(self):
		print("Current Stack:")
		print("bottom ", self.stack, " top")

	def setNonTerms(self):
		for rule in sef.gram.getRules():
			self.non_terms.add(rule.getVariable())
	def setTerms(self):
		for rule in self.gram.getRules():
			for yld in rule.getYield():
				for sub in yld:
					self._terms | (set(char for char in sub) & self._non_terms)
	
					
