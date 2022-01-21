import sys
from pprint import pprint
import pyparsing as pp
ppc = pp.pyparsing_common

def operatorOperands(tokenList):
	it = iter(tokenList)
	while True:
		try:
			yield (next(it), next(it))
		except StopIteration:
			break

class EvalConstant:
	def __init__(self, tokens):
		self.value = tokens[0]
	
	def eval(self):
		return int(self.value)

class EvalMultAdd:
	def __init__(self, tokens):
		self.value = tokens[0]
	
	def eval(self):
		result = self.value[0].eval()
		for op, val in operatorOperands(self.value[1:]):
			if op == "+":
				result += val.eval()
			if op == "*":
				result *= val.eval()
		return result

class EvalMult:
	def __init__(self, tokens):
		self.value = tokens[0]
	
	def eval(self):
		result = self.value[0].eval()
		for op, val in operatorOperands(self.value[1:]):
			if op == "+":
				result += val.eval()
			if op == "*":
				result *= val.eval()
		return result

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.readlines()
	
	##### Part 1: evaluate all expressions in the manner described in the
	##### statement, and output the sum of the results
	
	op = pp.oneOf("+ *")
	integer = pp.Word(pp.nums)
	integer.setParseAction(EvalConstant)
	expr = pp.infixNotation(integer, [ (op, 2, pp.opAssoc.LEFT, EvalMultAdd) ])
	
	total = 0
	for e in text:
		# print(e)
		res = expr.parseString(e)[0]
		# print(res.eval())
		total += res.eval()
	
	print(total)
	
	##### Part 1: same, but now addition has higher precedence than multiplication
	
	integer = pp.Word(pp.nums)
	integer.setParseAction(EvalConstant)
	expr = pp.infixNotation(integer, [ ("+", 2, pp.opAssoc.LEFT, EvalMultAdd), ("*", 2, pp.opAssoc.LEFT, EvalMultAdd) ])
	
	total = 0
	for e in text:
		# print(e)
		res = expr.parseString(e)[0]
		# print(res.eval())
		total += res.eval()
	
	print(total)