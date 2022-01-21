import sys

SUM = 2020

# nums should be sorted
def find2SUM(nums, target_sum):
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
		return None
	else:
		return nums[i] * nums[j]

# nums should be sorted
def find3SUM(nums, target_sum):
	n = len(nums)
	for i in range(n-1):
		left = i + 1
		right = n - 1
		while left < right:
			s = nums[i] + nums[left] + nums[right]
			if s == target_sum:
				break
			elif s > target_sum:
				right -= 1
			else:
				left += 1
		
		result = nums[i] + nums[left] + nums[right]
		if result == target_sum:
			break
	
	if result != target_sum:
		return None
	else:
		return nums[i] * nums[left] * nums[right]

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"

	with open(filename, "rt") as infile:
		text = infile.read()
	nums = [int(x) for x in text.split("\n")[:-1]]
	
	nums.sort()
	s = find3SUM(nums, SUM)
	
	if s == None:
		print("Some error")
	else:
		print(s)