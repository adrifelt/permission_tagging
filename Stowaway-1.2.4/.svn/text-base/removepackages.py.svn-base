#!/usr/bin/python

import sys, re, os

packages = []
lines = []

def readPackages(filename):
	global methodmap
	f = open(filename)
	for line in f:
		packages.append(line.rstrip())
	f.close()

def readFailedSinks(filename):
	global methodmap
	f = open(filename)
	for line in f:
		#print line.rstrip()
		flag = True
		for package in packages:
			pattern = re.compile(package)
			if pattern.match(line.rstrip()):
				flag = False
		if flag:
			lines.append(line.rstrip())
		#print flag
	f.close()
	
def main():
	readPackages("packages.txt")
	readFailedSinks(sys.argv[1])
	for line in lines:
		print line
	
if __name__ == "__main__":
    main()