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

	def setGrammar(self, gram):
		self.gram = gram
		self.setNonTerms()
		self.setTerms()
		self.populateParsetable()
		self.stack = ['$', 'S']

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
	def resetstack(self):
		self.stack = ['$', 'S']

	#this is only LL[1] right now, must be unambiguous, non recursive
	def parse(self, string):
		
		print("")
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
				self.describeStack()
				i+=1

			else:
				try:
					rule_i = list(self.parsetable[char][stack.pop()])[0]
				#	i-=1

				except IndexError:
					return False
				ops.append(rule_i)
				#for t in range(len(self.gram[rule_i].getYield()[0])-1, 0, -1):
				#	stack.append(self.gram[rule_i].getYield()[0][t])
				for t in self.gram[rule_i].getYield()[0][::-1]:
					stack.append(t)
				self.describeStack()
				
		if stack == []:
			return True
		else:
			return False
					

