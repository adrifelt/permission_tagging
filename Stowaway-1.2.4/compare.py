#!/usr/bin/python

import sys, re, os

manifestpermissions = []
foundpermissions_plain = []
foundpermissions_or = []
under = [] # our permissions that aren't in their manifest (underprivilege)
over = [] # their permissions that aren't in our list (overprivilege)

def readManifest(filename):
	global manifestpermissions
	f = open(filename)
	androidpattern = re.compile("android.permission.+",re.IGNORECASE)
	bookmarkpattern = re.compile("com.android.browser.permission..+_history_bookmarks",re.IGNORECASE);
	for line in f:
		if androidpattern.match(line):
			manifestpermissions.append(line.rstrip())
		elif bookmarkpattern.match(line):
			manifestpermissions.append(line.rstrip())

def readOurPerms(filename):
	global foundpermissions_plain
	global foundpermissions_or
	f = open(filename)
	or_pattern = re.compile('.+ or .+', re.IGNORECASE)
	for line in f:
		line = line.rstrip()
		if or_pattern.match(line): 
			foundpermissions_or.append(line)
		else:
			foundpermissions_plain.append(line)
		
# What permissions of ours do they not have?
def findUnderprivilege():
	global foundpermissions_plain
	global under
	for perm in foundpermissions_plain:
		if perm in manifestpermissions:
			pass
		else:
			under.append(perm)
	for orclause in foundpermissions_or:
		perms = orclause.split(" or ")
		found = False
		for perm in perms:
			if perm in manifestpermissions:
				found = True
			if perm == "NONE":
				found = True
		if not found:
			under.append(orclause)
	if len(under) > 0:
		f = open(sys.argv[3]+"/Underprivilege","w")
		for line in under:
			f.write(line+"\n")
		f.close()
			
# What permissions of theirs do we not think they need?
def findOverprivilege():
	for perm in manifestpermissions:
		if perm in foundpermissions_plain:
			pass # we both have it
		else:
			# lets see if its in an OR clause
			found = False
			for orclause in foundpermissions_or:
				ors = orclause.split(" or ")
				if perm in ors:
					found = True
			if not found:
				over.append(perm)
	if len(over) > 0:
		f = open(sys.argv[3]+"/Overprivilege","w")
		for line in over:
			f.write(line+"\n")
		f.close()
				

# Arg1 - their manifest
# Arg2 - our generated permissions	
# Arg3 - path for writing out
def main():
	readManifest(sys.argv[1])
	readOurPerms(sys.argv[2])
	findUnderprivilege()
	#print len(under)
	findOverprivilege()
	#print len(over)

if __name__ == "__main__":
    main()