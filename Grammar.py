#uses / as empty string and wont handle whitespace
from Rule import Rule
class Grammar:
	def __init__(self):
		self.length = 0
		self.rules = [] #consider dictionary,but adds sme redundancy
		#initialize with a call to readGrammar	
	
	def getLength(self):
		return self.length
	
	def __getitem__(self, k):
		if k > self.length:
			print("No such rule")
			return
		for rule in self.rules:
			if k <= rule.getLength():
	#			print("K is less than rule, so printing")
				return rule[k]
			else:
				k-=rule.getLength()
	def getRuleRange(self, V):
		ret=[None,None]
		for i in range(1,self.length+1):
			if 	self[i].getVar() == V and ret[0] == None:
				ret[0]=i
			if self[i].getVar()!= V and ret[0] != None:
				ret[1]=i
		if ret[1] == None:
			ret[1] = i+1
		return ret

	def getRule(self, V):
		for rule in self.rules:
			if rule.getVar() == V:
				return rule
		return False
	
	def readGrammar(self, f):
		try:
			with open(f, 'r') as _file:
				lines = _file.readlines()
				for line in lines:
					self.addRule(line)
		except Exception as e:
			print("Something went wrong reading the grammar")
			raise(e)
			
	def checkRecursion(self): #For now no way to remove recursion
	#	print("Checking for recursion")	
		rec = False
		for rule in self.rules:
			if rule.isRecursive():
				return True
		return False
	
	def removeRecursion(self): #For now no way to remove recursion, only redundancy
	#	print("Removing Redundancy")
		for rule in self.rules:
			if rule.isRedundant():
				rule.removeRedundancy()
				if rule is None:
					self.rules.remove(rule)

	def __str__	(self):
		return "\n".join([str(rule) for rule in self.rules])
	
	def removeRule(self, line):
		to_remove = Rule(line)
		for rule in self.rules:
			#rule = self.Rules[i]
			if rule.getVar() == to_remove.getVar():
				ylds = rule.getYield()
				for sub in to_remove.getYield():
					ylds.remove(sub)
				rule.setYield(ylds)
				if ylds == []:
					self.Rules.remove(rule)
				break
	def getRules(self):
		return self.rules
	
	def addRule(self, line):
		to_add = Rule(line)
	#	print("to_add is", to_add, "from", line)
		for rule in self.rules:
			if to_add.getVar() == rule.getVar():
				for sub in to_add.getYield():
					if sub not in rule.getYield():
						self.length+=1
						rule.addYield(sub)
				return
		self.rules.append(to_add)
	#	print("adding", to_add, "length is", to_add.length)
		self.length+=to_add.length
		
