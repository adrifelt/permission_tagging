#!/usr/bin/python

#Zhengyang Qu,
#Department of EECS, Northwestern University
#11/25/2011
#depack all the .apk files


import os,time
import json

class Depack:
  def __init__(self,sourcepath):
    self.sourcepath=sourcepath
    pass
    
  def depackage(self): 
    maindict={}
    rootDir=self.sourcepath
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
				maindict[appname]=finalpermissions
				count=count+1
				#print count


    print json.dumps(maindict)
    #for (k,v) in maindict.iteritems():
    	#print k + ":"
        #print v
    #print count


if __name__=="__main__":
  dep=Depack("/home/zyqu/res1/")
  dep.depackage()
