import sys
from pprint import pprint

FIELD_NAMES = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"] #, "cid"]

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read()
	
	passports = [pp.split() for pp in text.split("\n\n")]
	## pprint(passports)
	
	##### Part 1: find how many passports are there which have
	##### all the required fields - "cid" is optional
	
	n_valid = 0
	for pp in passports:
		fields_set = set([pair.split(":")[0] for pair in pp])
		if all(key in fields_set for key in FIELD_NAMES):
			n_valid += 1
	
	print(n_valid)
	
	##### Part 2: find how many passports are there which have
	##### all the required fields - "cid" is optional - and satisfy
	##### the appropriate constraints for each field.
	
	# transform passports to dicts
	passports = [dict([pair.split(":") for pair in pp]) for pp in passports]
	# pprint(passports)
	# print(len(passports))
	
	n_valid = 0
	# valid_list = []
	for pp in passports:
		validity_test = all([key in pp for key in FIELD_NAMES]) \
						and 1920 <= int(pp["byr"]) <= 2002 \
						and 2010 <= int(pp["iyr"]) <= 2020 \
						and 2020 <= int(pp["eyr"]) <= 2030 \
						and ((pp["hgt"].endswith("cm") and 150 <= int(pp["hgt"].rstrip("cm")) <= 193) \
							or (pp["hgt"].endswith("in") and 59 <= int(pp["hgt"].rstrip("in")) <= 76)) \
						and pp["hcl"].startswith("#") and len(pp["hcl"]) == 7 and all([x in "0123456789abcdef" for x in pp["hcl"][1:]]) \
						and (pp["ecl"] == "amb" or pp["ecl"] == "blu" or pp["ecl"] == "brn" or pp["ecl"] == "gry" or pp["ecl"] == "grn" or pp["ecl"] == "hzl" or pp["ecl"] == "oth") \
						and len(pp["pid"]) == 9 and pp["pid"].isdecimal()
	
		if validity_test:
			# valid_list.append(pp)
			n_valid += 1
	
	print(n_valid)
	# pprint(valid_list)