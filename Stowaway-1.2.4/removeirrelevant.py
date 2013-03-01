#!/usr/bin/python

import sys, re, os

patterns = ['android/','com/android/','com/htc/net/wimax/','java/','\*\*']
lines = []

def readFailedSinks(filename):
	global methodmap
	f = open(filename)
	for l in f:
		line = l.rstrip().lstrip()
		splitter = line.split(" ")
		flag = False
		for index,elem in enumerate(splitter):
			if index > 0:
				for patt in patterns:
					pattern = re.compile(patt)
					if pattern.match(elem):
						flag = True
						break
		if flag:
			lines.append(line.rstrip())
	f.close()
	
def main():
	readFailedSinks(sys.argv[1])
	for line in lines:
		print line
	
if __name__ == "__main__":
    main()