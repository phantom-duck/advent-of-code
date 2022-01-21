import sys
from pprint import pprint
import re

def rule2regexp(rules, rule_idx, defaults={}):
	if rule_idx in defaults:
		return defaults[rule_idx]
	
	# print("------")
	# print(rule_idx)
	# print(rules[rule_idx])
	# print(rules[rule_idx][0][0])
	# print("------")
	if type(rules[rule_idx][0][0]) == str:
		return rules[rule_idx][0][0]
	
	ret = "("
	for clause in rules[rule_idx]:
		for subrule in clause:
			# print(rule_idx, subrule)
			# print(ret)
			subexp = rule2regexp(rules, subrule)
			# print(subexp)
			ret += subexp
		ret += "|"
	ret = ret[:-1] + ")"
	
	return ret

def rule_startswith(rules, rule_idx):
	if type(rules[rule_idx][0][0]) == str:
		return set(rules[rule_idx][0][0])
	
	setx = set()
	for clause in rules[rule_idx]:
		setx = setx.union(rule_startswith(rules, clause[0]))
	return setx

def rule_endswith(rules, rule_idx):
	if type(rules[rule_idx][0][0]) == str:
		return set(rules[rule_idx][0][0])
	
	setx = set()
	for clause in rules[rule_idx]:
		setx = setx.union(rule_startswith(rules, clause[0]))
	return setx

def match_equals(regexp1, regexp2, string):
	if string == '':
		return True
	
	for i in range(len(string)):
		for j in range(i, len(string)):
			first = string[:i]
			middle = string[i:j]
			last = string[j:]
			if regexp1.fullmatch(first) and regexp2.fullmatch(last) and match_equals(regexp1, regexp2, middle):
				return True

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read().split("\n\n")
	
	rules_raw = [(int(rule.split(": ")[0]), rule.split(": ")[1]) for rule in text[0].split("\n")]
	messages = text[1].split()
	
	##### Part 1: count the messages that completely match rule 0
	
	rules = [0] * (max(x for (x,y) in rules_raw) + 1)
	for r, rhs in rules_raw:
		if rhs.startswith("\""):
			print(r)
			print(rhs)
			rules[r] = [[rhs[1]]]
			print(rules[r])
		else:
			rules[r] = [list(map(int, conc.split())) for conc in rhs.split("|")]
	
	# pprint(rules)
	# print(rule2regexp(rules, 0))
	
	expr = re.compile(rule2regexp(rules, 0))
	
	total = 0
	for msg in messages:
		if expr.fullmatch(msg):
			total += 1
	
	print(total)
	
	##### Part 2: change the rules 8 and 11 into the recursive versions below
	
	rules[8] = [[42], [42, 8]]
	rules[11] = [[42, 31], [42, 11, 31]]
	
	# print(rule2regexp(rules, 42))
	# print(rule2regexp(rules, 31))
	
	regexp42 = re.compile(rule2regexp(rules, 42))
	regexp31 = re.compile(rule2regexp(rules, 31))
	regexp8 = re.compile("(" + rule2regexp(rules, 42) + "+)")
	
	print(regexp31.match(""))
	print(regexp42.match(""))
	print(regexp8.match(""))
	
	## FIRST - LAST trial. Failure, all can start and end with a, b
	# print("  Rule 8:")
	# print(rule_startswith(rules, 8))
	# print(rule_endswith(rules, 8))
	# print("  Rule 42:")
	# print(rule_startswith(rules, 42))
	# print(rule_endswith(rules, 42))
	# print("  Rule 31:")
	# print(rule_startswith(rules, 31))
	# print(rule_endswith(rules, 31))
	
	total = 0
	for msg in messages:
		flag = False
		for i in range(len(msg)):
			if regexp8.fullmatch(msg[:i]):
				# print("yes")
				if match_equals(regexp42, regexp31, msg[i:]):
					print("yessss")
					flag = True
				# rest = msg[i+1:]
				# for j in range(len(rest)):
					# part42 = rest[:j]
					# part31 = rest[j+1:]
					# if any(x != '' for x in regexp42.split(part42)) or any(x != '' for x in regexp31.split(part31)):
						# continue
					# if len(regexp42.findall(part42)) == len(regexp31.findall(part31)):
						# flag = True
		
		if flag:
			total += 1
	
	print(total)