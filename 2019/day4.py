def check_num(num, lower=0, upper=999999):
	flag = True
	flag = flag and len(str(num))==6
	flag = flag and num >= lower and num <= upper
	
	forward_dif = [int(x) - int(y) for (x, y) in zip(str(num)[1:], str(num)[:-1])]
	flag1 = False
	for i in range(len(forward_dif)):
		if forward_dif[i] < 0:
			flag1 = False
			break
		elif forward_dif[i] == 0 and (i == 0 or forward_dif[i-1] != 0) and (i == len(forward_dif) - 1 or forward_dif[i+1] != 0):
			flag1 = True
	
	return flag and flag1