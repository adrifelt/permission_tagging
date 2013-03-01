#!/usr/bin/python

import sys, re, os

methodmap = {}
foundclasses = []
orphans = []

def readMethodMap(filename):
	global methodmap
	f = open(filename)
	for line in f:
		signature = line.rstrip()
		signatureS = signature.split(".")
		method = signatureS[len(signatureS)-1]
		clazz = ""
		for i in range(len(signatureS)-1):
			clazz += signatureS[i]
			if i < len(signatureS)-2:
				clazz += "."
		if method in methodmap:
			methodmap[method].append(clazz)
		else:
			methodmap[method] = [ clazz ]
	f.close()
	
def readOrphans(filename):
	f = open(filename)
	obj_pattern = re.compile("^java.lang.Object")
	unk_pattern = re.compile("^\*\*unknown")
	for line in f:
		lineS = line.rstrip()
		if obj_pattern.match(lineS) or unk_pattern.match(lineS):
			split = lineS.split("/")
			if len(split) <= 1:
				split2 = lineS.split(".")
				if len(split2) > 1:
					orphans.append(split2[len(split2)-1])
			else:
				orphans.append(split[len(split)-1])
	f.close()
	
def readOrphansDebug(filename):
	f = open(filename)
	obj_pattern = re.compile("^java.lang.Object")
	unk_pattern = re.compile("^\*\*unknown")
	for line in f:
		linesplit = line.split(" ")
		if len(linesplit) == 3:
			lineS = linesplit[2].rstrip()
			if obj_pattern.match(lineS) or unk_pattern.match(lineS):
				split = lineS.split("/")
				if len(split) <= 1:
					split2 = lineS.split(".")
					if len(split2) > 1:
						orphans.append(split2[len(split2)-1])
				else:
					orphans.append(split[len(split)-1])
	f.close()
	
def readFoundClasses(filename):
	f = open(filename)
	and_pattern1 = re.compile('^android.*')
	and_pattern2 = re.compile('^com.android.*')
	net_pattern = re.compile('^java.net.*')
	for line in f:
		lineS = line.rstrip()
		if and_pattern1.match(lineS) or and_pattern2.match(lineS) or net_pattern.match(lineS):
			foundclasses.append(lineS)
	
def main():
	readMethodMap("methodlist.txt")
	readFoundClasses(sys.argv[1])
	readOrphansDebug(sys.argv[2])
	if len(orphans) > 0:
		if len(foundclasses) > 0:
			for orphan in orphans:
				if orphan in methodmap:
					#print "Found in map: " + orphan 
					#print methodmap[orphan]
					for clazz in methodmap[orphan]:
						#print clazz
						if clazz in foundclasses:
							print clazz + "." + orphan
				#if resolved:
				#	print "Resolved: " + resolvedstr
				#else:
				#	print "Unresolved: " + orphan
	
if __name__ == "__main__":
    main()