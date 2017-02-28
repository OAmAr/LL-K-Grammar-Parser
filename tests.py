#!/usr/bin/python3

import unittest
from Grammar import Grammar
from Parser import Parser
from Rule import Rule

class TestParser():#unittest.TestCase):
	def atestCreate(self):
		P=Parser()
		G = Grammar()
		G.readGrammar('gram1.txt')
		P.setGrammar(G)
		#P.describe()
	
	def atestCreate(self):
		P=Parser()
		G = Grammar()
		G.readGrammar('gram1.txt')
		P.setGrammar(G)
		self.assertEqual(P._non_terms, set(["S", "A"]))
		self.assertEqual(P._terms, set(["0", "1", "$"]))
	
	def testtable1(self):
		P=Parser()
		G = Grammar()
		G.readGrammar('gram1.txt')
		P.setGrammar(G)
		print(P.parsetable)
		#self.assertEqual(P.parsetable, {'0' : {'S':set([1]),'A': set()} , '1':{'S':set(),'A': set([3])}, '$': {'S':set(),'A': set()}})

	def atesttable2(self):
		P=Parser()
		G = Grammar()
		G.readGrammar('gram2.txt')
		P.setGrammar(G)
		#print(P.parsetable)
		self.assertEqual(P.parsetable, {'0' : {'S':set([1]),'A': set()} , '1':{'S':set([3]),'A': set([4])}, '$': {'S':set(),'A': set()}})

	def atestParser_no_follow(self):
		P=Parser()
		G = Grammar()
		G.readGrammar('gram1.txt')
		P.setGrammar(G)
		self.assertTrue(P.parse("01"))
		self.assertFalse(P.parse("0"))
		#self.assertTrue(P.parse("0011"))
	
	def atestParser_first(self):
		P=Parser()
		G = Grammar()
		G.readGrammar('gram1.txt')
		P.setGrammar(G)
		P.buildFirstsets()
		print(P.firstsets)
		#print(P.firstSet('S'))

class TestGrammar(unittest.TestCase):
	def test_create_grammar(self):
		G = Grammar()
		G.addRule("A	A | /")
		self.assertEqual(str(G), "A ---> A | /")
	def test_range(self):
		G=Grammar()
		G.readGrammar('gram1.txt')
		self.assertEqual(G.getRuleRange('A'), set([3]))
	def test_remove(self):
		G =Grammar()
		G.addRule("A	A | /")
		self.assertEqual(str(G), "A ---> A | /")
		G.removeRule("A 	A")
		self.assertEqual(str(G), "A ---> /")
	
	def test_add(self):
		G=Grammar()
		G.addRule("A	A")
		self.assertEqual(str(G), "A ---> A")
		G.addRule("A	/")
		self.assertEqual(str(G), "A ---> A | /")
	
	def test_rec_check(self):
		G=Grammar()
		G.addRule("A	A | /")
		self.assertTrue(G.checkRecursion())
			
	def test_rec_rem(self):
		G=Grammar()
		G.addRule("A	A | /")
		G.removeRecursion()
		self.assertEqual(str(G), "A ---> /")
	
	def test_index(self):
		G=Grammar()
		G.addRule("A	A | /")
		self.assertEqual(str(G[1]), "A ---> A")
		self.assertEqual(str(G[2]), "A ---> /")

	def test_multiple_adds(self):
		G=Grammar()
		G.addRule("A	AB | /")
		G.addRule("B	Ab | /")
		#print("")
		#print(G)

	def test_grammar_from_file(self):
		G=Grammar()
		G.readGrammar('gram1.txt')
	#	print("")
	#	print(G)

class TestRules(unittest.TestCase):
	def test_rule_simple(self):
		r1 = Rule("A	/")
		self.assertEqual(r1.non, "A")
		self.assertEqual(r1.yld, ["/"])

	def test_rule_multi(self):
		r1 = Rule("A	A | /")
		self.assertEqual(r1.non, "A")
		self.assertEqual(r1.yld, ["A","/"])

	def test_rule_str(self):
		r1 = Rule("A	A | /")
		#print(r1)
		self.assertEqual(str(r1), "A ---> A | /")
	def test_add_sub(self):
		r1 = Rule("A 	A")
		self.assertEqual(r1.getYield(), ["A"])
		r1.addYield("/")
		self.assertEqual(r1.yld, ["A","/"])
		


if __name__ == '__main__':
	unittest.main()
