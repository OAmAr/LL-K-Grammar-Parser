from Parser import Parser
from Grammar import Grammar
#P = Parser()
#G = Grammar()
#G.readGrammar('gram1.txt')
#P.setGrammar(G)
#for string in ['0','01','11','0011','10']:
#	P.parse(string)
#	input()

P = Parser()
G = Grammar()
G.readGrammar('gram3.txt')
P.setGrammar(G)

for string in['()', '(a+a)']: #['(a+a)','a','a+a','((a+a)+a)']:
	P.parse(string)
	input()
