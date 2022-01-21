import sys
from typing import List

if __name__=="__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "input.txt"
	
	with open(filename) as infile:
		text = infile.read()
	text = text.replace("\n", "").replace(" ", "")
	
	width = 25
	height = 6
	
	layers = [text[i: i + width * height] for i in range(0, len(text), width * height)]
	
	##### Part one
	min = len(text) + 1
	for layer in layers:
		zeros = len([x for x in layer if x=='0'])
		if zeros < min:
			min = zeros
			min_layer = layer
	
	print(len([x for x in min_layer if x=='1']) * len([x for x in min_layer if x=='2']))
	
	##### Part two
	out_img = ['2'] * (width * height)
	
	for layer in layers:
		for i in range(width * height):
			if out_img[i] != '2':
				continue
			out_img[i] = layer[i]
	
	out_img = [''.join(out_img[i: i + width]) for i in range(0, width * height, width)]
	out_img = [row.replace('0',' ') for row in out_img]
	for row in out_img:
		print(row)