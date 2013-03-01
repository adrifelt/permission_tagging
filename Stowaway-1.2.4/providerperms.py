#!/usr/bin/python

import sys, re, os

providermap = {}
permissions = []

def readProviderMap(filename):
	global providermap
	f = open(filename)
	for line in f:
		lineS = line.split(",")
		providermap[lineS[0]] = lineS[1].rstrip()
	f.close()
	
def readStringList(filename):
	global permissions
	f = open(filename)
	and_pattern = re.compile('.+ and .+',re.IGNORECASE)
	for line in f:
		lineS = line.split(" ")
		uri = lineS[0].rstrip("/")
		if not checkMap(uri):
			parts = uri.split("/")
			partialuri = ""
			for part in parts:
				if (part != "content:"):
					partialuri = partialuri + "/" + part
					checkMap(partialuri)
				else:
					partialuri = part

def checkMap(uri):
	global providermap
	and_pattern = re.compile('.+ and .+',re.IGNORECASE)
	if uri in providermap:
		perm = providermap[uri]
		if and_pattern.match(perm):
			perms = perm.split(" and ")
			for i in perms:
				print i
		else:
			print perm
		sys.stderr.write(uri+" ["+perm+"]\n")
		return True
	else:
		return False
				

def main():
	readProviderMap("providermap.csv");
	readStringList(sys.argv[1])

if __name__ == "__main__":
    main()


