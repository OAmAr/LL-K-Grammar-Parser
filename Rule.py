class Rule:
	def __init__(self,line):
		parsed = self.parse(line)
		self.non=parsed[0]
		self.yld=parsed[1]
	
	def getVar(self):
		return self.non
	def setVar(self, x):
		self.non = x
	def getYield(self):
		return self.yld
	def setYield(self, L):
		self.yld = L
	
	def addYield(self, line):
		for yld in line.split("|"):
			self.yld.append(yld)

	def parse(self, line):
		ret = (line[0], [])
		for el in line[1:].split("|"):
			ret[1].append(el.strip())
		return ret
	
	def isRedundant(self): #checks if rule produces only itself
		red = False
		for yld in self.yld:
			red = red or self.non==yld
		return red
	
	def isRecursive(self): #checks if directly left recursive
		rec = False
		for yld in self.yld:
			rec = rec or self.non==yld[0]
		return rec
	def removeRedundancy(self):
		if self.isRedundant():
			for sub in self.yld:
				if sub == self.non:
					self.yld.remove(sub)
			if self.yld == []:
				self = None
	def __str__(self):
		return str(self.non+ " ---> "+" | ".join(self.yld))
