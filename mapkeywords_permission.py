#!/usr/bin/python

#Zhengyang Qu,
#Department of EECS, Northwestern University
#03/05/2013

import os, json

class Map:
  def __init__(self):
    pass

  def getpermissionfrequency(self,keyworddict,permissiondict):
    kwdict={}
    kwcount=0
    maindict={}
#the times a key word found
    threshold=8

    for (k,v) in keyworddict.iteritems():
	for elem in v:
		if elem not in kwdict:
			kwdict[elem]=1
		if elem in kwdict:
			kwdict[elem]=kwdict[elem]+1

    kwlist=[]
    for kkey in kwdict:
	if kwdict[kkey]>threshold:
		kwlist.append(kkey)
		kwcount=kwcount+1
    #print kwcount

    for elem in kwlist:
	
	permissionmap={}
	orderedlist=[]

	for (k,v) in keyworddict.iteritems():
		for targetkw in v:
			if elem==targetkw:
				thispermisions=permissiondict[k]
				for pm in thispermisions:
					if pm not in permissionmap:
						permissionmap[pm]=1
					if pm in permissionmap:
						permissionmap[pm]=permissionmap[pm]+1

	for kperm in permissionmap:
		permissionmap[kperm]=(permissionmap[kperm]*100.0)/kwdict[elem]

	orderedlist=sorted(permissionmap.iteritems(), key=lambda d:d[1], reverse=True)
	maindict[elem]=orderedlist

    return maindict


  def getkeywordfrequency(self,keyworddict,permissiondict):
    permlist=[]
    permcount=0
    maindict={}
    for (k,v) in permissiondict.iteritems():
	for elem in v:
		if elem not in permlist:
			permlist.append(elem)
			permcount=permcount+1
    #''print permcount

    for elem in permlist:

        totalthisperm=0
	keywordmap={}
	orderedlist=[]	

	for (k,v) in permissiondict.iteritems():
		for perm in v:
			if perm==elem:
				totalthisperm=totalthisperm+1
				thiskeywords=keyworddict[k]
				for kw in thiskeywords:
					if kw not in keywordmap:
						keywordmap[kw]=1
					if kw in keywordmap:
						keywordmap[kw]=keywordmap[kw]+1

	for kkey in keywordmap:
		keywordmap[kkey]= (keywordmap[kkey]*100.0)/totalthisperm

	orderedlist=sorted(keywordmap.iteritems(), key=lambda d:d[1], reverse=True)
	maindict[elem]=orderedlist

    return maindict
		 					


    

  def getkeyword(self,sourcepath, permissiondict):
    file_object=open(sourcepath)

    try:
    	alllines = file_object.readlines()
        maindict={}
	apkname=''
	keywords=[]
	for line in alllines:
		line=line.strip()
		if line.find('.apk')==(len(line)-4):
			apkname=line
			continue
		if len(line)==0:
			if len(apkname)>0 and (apkname not in maindict):
				maindict[apkname]=keywords
			keywords=[]
			apkname=''
			continue
		keywords.append(line)
    finally:
        file_object.close()
	kwdict={}
	for kkey in maindict:
		if kkey in permissiondict:
			kwdict[kkey]=maindict[kkey]
    	return kwdict


  def getperm(self,sourcepath): 
    maindict={}
    rootDir=sourcepath
    list_dirs=os.walk(rootDir)
    count=0
    for root, dirs, files in list_dirs:
	for d in dirs:       
        	level2rootDir=os.path.join(root, d)
		appname=os.path.basename(level2rootDir)
		if appname.find('.apk')==(len(appname)-4):
			list_files=os.walk(level2rootDir)
			fileslist=[]
			origpermissions=[]
			ourpermissions=[]
			overpermissions=[]
			underpermissions=[]
			for root2, dirs2, files2 in list_files:
				for f in files2:
					filename=os.path.join(root2,f)
					filebasename=os.path.basename(filename)
					fileslist.append(filebasename)
					if filebasename =='orig':
						file_object=open(filename)
						try:
							alllines = file_object.readlines()
							for line in alllines:
								line=line.strip()
								ContainOr=1
								if line.find(' or ')==-1:
									ContainOr=0
									if (line not in origpermissions) and line != 'NONE':
										origpermissions.append(line)
										continue

								first='XXXX'
								remain=line
								while ContainOr==1:
									first=remain[:remain.find(' or ')]
									remain=remain[remain.find(' or ')+4:]
									if (first not in origpermissions) and first!='NONE':
										origpermissions.append(first)
									if remain.find(' or ')<0:
										ContainOr=0
										break
								if (remain not in origpermissions) and remain!='NONE':
									origpermissions.append(remain)

						finally:
							file_object.close()
					if filebasename =='OurPermissions':
						file_object=open(filename)
						try:
							alllines = file_object.readlines()
							for line in alllines:
								line=line.strip()
								ContainOr=1
								if line.find(' or ')==-1:
									ContainOr=0
									if (line not in ourpermissions) and line != 'NONE':
										ourpermissions.append(line)
										continue

								first='XXXX'
								remain=line
								while ContainOr==1:
									first=remain[:remain.find(' or ')]
									remain=remain[remain.find(' or ')+4:]
									if (first not in ourpermissions) and first!='NONE':
										ourpermissions.append(first)
									if remain.find(' or ')<0:
										ContainOr=0
										break
								if (remain not in ourpermissions) and remain!='NONE':
									ourpermissions.append(remain)
						finally:
							file_object.close()
					if filebasename =='Overprivilege':
						file_object=open(filename)
						try:
							alllines = file_object.readlines()
							for line in alllines:
								line=line.strip()
								if (line not in overpermissions) and line != 'NONE':
									overpermissions.append(line)
						finally:
							file_object.close()
					if filebasename =='Underprivilege':
						file_object=open(filename)
						try:
							alllines = file_object.readlines()
							for line in alllines:
								line=line.strip()
								ContainOr=1
								if line.find(' or ')==-1:
									ContainOr=0
									if (line not in underpermissions) and line != 'NONE':
										underpermissions.append(line)
										continue

								first='XXXX'
								remain=line
								while ContainOr==1:
									first=remain[:remain.find(' or ')]
									remain=remain[remain.find(' or ')+4:]
									if (first not in underpermissions) and first!='NONE':
										underpermissions.append(first)
									if remain.find(' or ')<0:
										ContainOr=0
										break
								if (remain not in underpermissions) and remain!='NONE':
									underpermissions.append(remain)
						finally:
							file_object.close()

			if 'AndroidManifest.xml' in fileslist and (len(origpermissions)>0 or len(ourpermissions)>0):
				finalpermissions=[]
				for elem in ourpermissions:
					if (elem in underpermissions) or (elem in origpermissions):
						finalpermissions.append(elem)
				if appname not in maindict:
					maindict[appname]=finalpermissions
					count=count+1


    return maindict

if __name__=="__main__":
  result=Map()
  permissiondict=result.getperm("/home/zyqu/res/")
  keyworddict=result.getkeyword("/home/zyqu/Research/Android_sec/parsexml/semant/fulloutput.txt", permissiondict)
  intersectpermissiondict={}
  for elem in permissiondict:
  	if elem in keyworddict:
		intersectpermissiondict[elem]=permissiondict[elem]

  #for k in keyworddict:
#	print k
#	for v in keyworddict[k]:
#		print v
  #print len(intersectpermissiondict)
  #print len(keyworddict)


  kwfreq=result.getkeywordfrequency(keyworddict,intersectpermissiondict)
  pmfreq=result.getpermissionfrequency(keyworddict,intersectpermissiondict)

  for k in kwfreq:
	print k
	for v in kwfreq[k]:
		print v
	print '\n',

  print '\n\n'
  print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

  for k in pmfreq:
	print k
	for v in pmfreq[k]:
		print v
	print '\n',





