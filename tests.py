#!/usr/bin/python3

import unittest
from Grammar import Grammar
from Parser import Parser
from Rule import Rule

#class TestParser(unittest.TestCase):
	#def test	

class TestGrammar(unittest.TestCase):
	def test_create_grammar(self):
		G = Grammar()
		G.addRule("A	A | /")
		self.assertEqual(str(G), "A ---> A | /")

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
	

	def test_multiple_adds(self):
		G=Grammar()
		G.addRule("A	AB | /")
		G.addRule("B	Ab | /")
		#print("")
		#print(G)

	def test_grammar_from_file(self):
		G=Grammar()
		G.readGrammar('gram1.txt')
		print("")
		print(G)

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
