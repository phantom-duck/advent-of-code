import sys

PREAMBLE_LENGTH = 25

def find2SUM(nums, target_sum):
	nums = nums[:]
	nums.sort()
	i = 0
	j = len(nums) - 1
	while i < j:
		s = nums[i] + nums[j]
		if s == target_sum:
			break
		elif s > target_sum:
			j -= 1
		else:
			i += 1
	
	if s != target_sum:
		return False
	else:
		return True

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.readlines()
	
	numbers = [int(x) for x in text]
	
	##### Part 1: find the first number which is not the sum of any two
	##### of the previous PREAMBLE_LENGTH numbers
	
	for i, n in enumerate(numbers):
		if i < PREAMBLE_LENGTH:
			continue
		
		if not find2SUM(numbers[i - PREAMBLE_LENGTH:i], n):
			res = n
			break
	
	print(res)

	##### Part 2: for the number n we found previously, we need to find
	##### a contiguous sublist of all the numbers which sums to n.
	
	run_sum = 0
	run_sums = [0]
	for n in numbers:
		run_sum += n
		run_sums.append(run_sum)
	
	left = 0
	right = 2
	while right < len(run_sums) and left < len(run_sums) - 2:
		cand = run_sums[right] - run_sums[left]
		
		if cand == res:
			print("hurrah")
			break
		elif cand > res:
			left += 1
			if right - left <= 1:
				right += 1
		else:
			right += 1
	
	max_inrange = max(numbers[left:right])
	min_inrange = min(numbers[left:right])
	
	print(max_inrange + min_inrange)