#!/usr/bin/python

#Zhengyang Qu,
#Department of EECS, Northwestern University
#03/05/2013

import os, json
from operator import mul

class Map:
  def __init__(self):
    pass


  def combovariation(self,keyworddict,permissiondict):
    permorder=1
    pmdict={}
    for (k,v) in permissiondict.iteritems():
	for elem in v:
		if elem not in pmdict:
			pmdict[elem]=permorder
			permorder=permorder+1
    file_op1=open('combovarpermindex.txt','w')
    try:
	lower=1
	upper=len(pmdict)
	while lower<=upper:
		for k in pmdict:
			if pmdict[k]==lower:
				file_op1.write(k)
				file_op1.write(', %s'%pmdict[k])
				file_op1.write('\n')
				lower=lower+1
    except:
	print 'fail to write file varpermindex.txt'
    finally:
	file_op1.close()

    threshold=2
    kwdict={}
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
    #rangprint 'How many keywords?\n%s'%len(kwlist)

    file_op2=open('combokwmatchperms.txt',"w")
    file_op3=open('combokwstep.txt',"w")
    file_op4=open('combokwindex.txt',"w")
    try:
	finalresnum=0
	combothreshold=2
	loopcount=1
	n=len(kwlist)
	totalcount=reduce(mul, range(1,n+1))/2/reduce(mul, range(1,n-2+1))
    	for i in range(len(kwlist)-1):
		for j in range(i+1,len(kwlist)):
			print 'Loop: %s'%loopcount+'/%s'%totalcount
			stepsize=0
			targetkw1=kwlist[i]
			targetkw2=kwlist[j]
			targetpermissions={}


			for targetapp in keyworddict:
				if (targetkw1 in keyworddict[targetapp]) and (targetkw2 in keyworddict[targetapp]):
					stepsize=stepsize+1
					targetpermissions[stepsize]=permissiondict[targetapp]
			
			

			if stepsize >= combothreshold:
				
				for keynum in targetpermissions:
					for valperm in targetpermissions[keynum]:
						file_op2.write('%s'%pmdict[valperm])
						file_op2.write('	')
					file_op2.write('\n')
				#file_op2.write('\n')

				file_op3.write('%s'%stepsize)
				file_op3.write('\n')

				file_op4.write(targetkw1+', '+targetkw2)
				file_op4.write('\n')
				finalresnum=finalresnum+1


			if stepsize < combothreshold:
				print 'Only %s samples'%stepsize+' less than %s'%combothreshold
			loopcount=loopcount+1
		
    except:
	print 'faile to write files combokwmatchperms.txt / combokwstep.txt / combokwindex.txt'

    finally:
	file_op2.close()
	file_op3.close()
	file_op4.close()
	print 'Number of keywords: %s'%finalresnum
		


  def variation(self,keyworddict,permissiondict):
    permorder=1
    pmdict={}
    for (k,v) in permissiondict.iteritems():
	for elem in v:
		if elem not in pmdict:
			pmdict[elem]=permorder
			permorder=permorder+1
    file_op1=open('varpermindex.txt','w')
    try:
	lower=1
	upper=len(pmdict)
	while lower<=upper:
		for k in pmdict:
			if pmdict[k]==lower:
				file_op1.write(k)
				#file_op1.write(', %s'%pmdict[k])
				file_op1.write('\n')
				lower=lower+1
    except:
	print 'fail to write file varpermindex.txt'
    finally:
	file_op1.close()

    threshold=0
    kwdict={}
    for (k,v) in keyworddict.iteritems():
	for elem in v:
		if elem not in kwdict:
			kwdict[elem]=1
		if elem in kwdict:
			kwdict[elem]=kwdict[elem]+1

    kwlist=[]
    for kkey in kwdict:
	if kwdict[kkey]>threshold:
		#print kwdict[kkey]
		#print threshold
		#print '\n'
		kwlist.append(kkey)
    #print 'How many keywords?\n%s'%len(kwlist)
    file_op2=open('kwmatchperms.txt',"w")
    file_op3=open('kwstep.txt',"w")
    file_op4=open('kwindex.txt',"w")
    try:
	loopcount=0
    	for elem in kwlist:
		loopcount=loopcount+1
		print 'Loop: %s'%loopcount+' in %s'%len(kwlist)
		stepsize=0
		for (k,v) in keyworddict.iteritems():
			for targetkw in v:
				if targetkw==elem:
					permissions=permissiondict[k]
					for targetperm in permissions:
						file_op2.write('%s'%pmdict[targetperm])
						file_op2.write('	')
					file_op2.write('\n')
					stepsize=stepsize+1
		file_op3.write('%s'%stepsize)
		file_op3.write('\n')
		file_op4.write(elem)
		file_op4.write('\n')
    except:
	print 'faile to write files kwmatchperms.txt / kwstep.txt / kwindex.txt'
    finally:
	file_op2.close()
	file_op3.close()
	file_op4.close()


  def chisquare(self,keyworddict,permissiondict):
    threshold=0
    pmdict={}
    permlist=[]  
    for (k,v) in permissiondict.iteritems():
	for elem in v:
		if elem not in pmdict:
			pmdict[elem]=1
		if elem in pmdict:
			pmdict[elem]=pmdict[elem]+1
    for pmkey in pmdict:
	if pmdict[pmkey]>threshold:
		permlist.append(pmkey)

    permkeydict={}   

    for elem in permlist:
	permkeylist=[]
	keywordmap={}
	for (k,v) in permissiondict.iteritems():
		for perm in v:
			if perm==elem:
				thiskeywords=keyworddict[k]
				for kw in thiskeywords:
					if kw not in keywordmap:
						keywordmap[kw]=1
					if kw in keywordmap:
						keywordmap[kw]=keywordmap[kw]+1
	for kw in keywordmap:
		permkeylist.append(kw)

	permkeydict[elem]=permkeylist

    maindict={}
    print 'Ready to Go!'
    loopcount=1
    for (targetperm,v) in permkeydict.iteritems():
	print 'Loop: %s'%loopcount+'/%s'%len(permkeydict)
	loopcount=loopcount+1
        chisqlist=[]
	print 'Number of keywords: %s'%len(v)
	for targetkw in v:
		#if loopcount==6:
			#print targetkw
		a=0
		b=0
		c=0
		d=0
		for apkname in permissiondict:
			if ((targetperm in permissiondict[apkname]) and (targetkw in keyworddict[apkname])):
				a=a+1
				continue
			if ((targetperm in permissiondict[apkname]) and (targetkw not in keyworddict[apkname])):
				b=b+1
				continue
			if ((targetperm not in permissiondict[apkname]) and (targetkw in keyworddict[apkname])):
				c=c+1
				continue
			if ((targetperm not in permissiondict[apkname]) and (targetkw not in keyworddict[apkname])):
				d=d+1
				continue
		#print 'before devision'
		if (a+b+c+d)>40:
			chisq=(a+b+c+d)* (abs(a*d-b*c)-0.5*(a+b+c+d)) * (abs(a*d-b*c)-0.5*(a+b+c+d)) *1.0/(a+b)/(c+d)/(b+d)/(a+c)
		if (a+b+c+d)<=40:
			chisq=(a+b+c+d)*(a*d-b*c)*(a*d-b*c)*1.0/(a+b)/(c+d)/(b+d)/(a+c)
		#print 'after devision'
		chisqlist.append(chisq)
	maindict[targetperm]=chisqlist		
    return maindict		
		
  def getpermissionfrequency(self,keyworddict,permissiondict):
    kwdict={}
    kwcount=0
    maindict={}
#the times a key word found
    threshold=5

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
    pmdict={}

#the times a key word found
    threshold=5

    for (k,v) in permissiondict.iteritems():
	for elem in v:
		if elem not in pmdict:
			pmdict[elem]=1
		if elem in pmdict:
			pmdict[elem]=pmdict[elem]+1


    for pmkey in pmdict:
	if pmdict[pmkey]>threshold:
		permlist.append(pmkey)
		permcount=permcount+1
    #for (k,v) in permissiondict.iteritems():
	#for elem in v:
	#	if elem not in permlist:
	#		permlist.append(elem)
	#		permcount=permcount+1
    #''print permcount

    for elem in permlist:

        #totalthisperm=0
	keywordmap={}
	orderedlist=[]	

	for (k,v) in permissiondict.iteritems():
		for perm in v:
			if perm==elem:
				thiskeywords=keyworddict[k]
				for kw in thiskeywords:
					if kw not in keywordmap:
						keywordmap[kw]=1
					if kw in keywordmap:
						keywordmap[kw]=keywordmap[kw]+1

	for kkey in keywordmap:
		keywordmap[kkey]= (keywordmap[kkey]*100.0)/pmdict[elem]

	orderedlist=sorted(keywordmap.iteritems(), key=lambda d:d[1], reverse=True)
	maindict[elem]=orderedlist

    return maindict
		 					
  def getkeyword(self,sourcepath, permissiondict):
    file_object=open(sourcepath)
    count=0

    try:
    	alllines = file_object.readlines()
        maindict={}
	apkname=''
	keywords=[]
	for line in alllines:
		line=line.strip()
		if line.find('.apk')>0:
			apkname=line
			continue
		if len(line)==0:
			if len(apkname)>0 and (apkname not in maindict):
				maindict[apkname]=keywords
				count=count+1
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
#test
		#if kkey not in permissiondict:
			#print kkey
	#print count
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
					#print filename
					
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
						except:
							print 'fail to open '+filename

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

						except:
							print 'fail to open '+filename

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
						except:
							print 'fail to open '+filename

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
						except:
							print 'fail to open '+filename


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
  keyworddict=result.getkeyword("/home/zyqu/Research/Android_sec/parsexml/semant/fullopt", permissiondict)
  #keyworddict=result.getkeyword("/home/zyqu/Research/Android_sec/parsexml/semant/catigorizations.txt", permissiondict)
  intersectpermissiondict={}
  for elem in permissiondict:
  	if elem in keyworddict:
		intersectpermissiondict[elem]=permissiondict[elem]


  result.combovariation(keyworddict,intersectpermissiondict)
 
  #result.variation(keyworddict,intersectpermissiondict)

  #print len(keyworddict)
  #print len(permissiondict)
  #print len(intersectpermissiondict)

  #chisqv=result.chisquare(keyworddict,intersectpermissiondict)
  #file_output=open("/home/zyqu/Research/Android_sec/parsexml/semant/genchisqres.txt","w")
  #try:
  	#for (k,v) in chisqv.iteritems():
		#file_output.write(k)
		#file_output.write('|||||')
		#for chival in v:
			#outstr = "%s"%chival+', '
			#file_output.write(outstr)
		#file_output.write('\n\n')
  #finally:
	#file_output.close() 

  #file_op1=open("/home/zyqu/Research/Android_sec/parsexml/semant/genchisqpermindex.txt","w")
  #file_op2=open("/home/zyqu/Research/Android_sec/parsexml/semant/gensqvals.txt","w")
  #try:
  	#for (k,v) in chisqv.iteritems():
		#file_op1.write(k)
		#file_op1.write('\n')
		#for sqval in v:
			#outstr = "%s"%sqval+'	'
			#file_op2.write(outstr)
		#file_op2.write('\n')

  #except:
	#print 'Errors on writing to the files: chisqpermindex.txt and sqvals.txt'
					
  #finally:
	#file_op1.close() 
	#file_op2.close()


  #kwfreq=result.getkeywordfrequency(keyworddict,intersectpermissiondict)
  #pmfreq=result.getpermissionfrequency(keyworddict,intersectpermissiondict)

  #for k in kwfreq:
	#print k
	#for v in kwfreq[k]:
		#print v
	#print '\n',

  #print '\n\n'
  #print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

  #for k in pmfreq:
	#print k
	#for v in pmfreq[k]:
		#print v
	#print '\n',

  #print len(keyworddict)
  #print len(permissiondict)
  #print len(intersectpermissiondict)


  





