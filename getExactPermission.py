#!/usr/bin/python

##Zhengyang Qu, EECS, Northwestern Univeristy, 02/22/2013##

import os
import json 

class ExactPermissionParser: 

	def __init__(self,path):
		self.path=path

	def GetExactPerm(self,path):
		list_dirs = os.walk(path) 
		packagenum=0
		nonoverprivnum=0
		overprivnum=0
		maindict={}
		for root, dirs, files in list_dirs: 
			for f in files:
				httplist=[]
				filepath=os.path.join(root, f)
				if filepath.find("res")>=0:
					file_object=open(filepath)
					OVERPRIVFDETECTED=0
					PERMISSIONSDETECTED=0
					packagename=''
					overprivs=[]
					permissions=[]
					try:
						alllines = file_object.readlines()
						for line in alllines:
							line=line.strip()

							if line.find('.apk')>=0 and (line.find('.apk')==(len(line)-4)):
								OVERPRIVFDETECTED=0
								PERMISSIONSDETECTED=0
								packagename=line[:len(line)-4]
								packagenum=packagenum+1
								continue

							if line.find("Stowaway does not think your application is overprivileged.")>=0: 
								nonoverprivnum=nonoverprivnum+1
								OVERPRIVFDETECTED=0
								overprivs=[]
								continue
							if line.find("Stowaway thinks your application has the following extra permissions:")>=0: 
								overprivs=[]
								OVERPRIVFDETECTED=1
								overprivnum=overprivnum+1
								continue

							if line=='Required Permissions': #line.find("Required Permissions")>=0:
								OVERPRIVFDETECTED=0
								continue

							if line.find("Here, we list the permission-protected API calls, Content Providers, and Intents")>=0:
								PERMISSIONSDETECTED=1
								continue

							if line=='Reflection Errors':
								PERMISSIONSDETECTED=0
								continue

							if OVERPRIVFDETECTED==1 and line.find('Required Permissions')==-1:
								overprivs.append(line)
								continue

							##handle the exact required permissions
							if PERMISSIONSDETECTED==1 and line.find('Reflection Errors')==-1:
								ContainOr=1
								if line.find('[')>=0 and line.find(']')>=0:
									temppermission=line[line.find('[')+1:line.find(']')]
									if  temppermission.find(' or ') <0:
										ContainOr=0
										if (temppermission not in permissions) and temppermission!='NONE':
											permissions.append(temppermission)
										continue
									first='XXXX'
									remain=temppermission
									while ContainOr==1:
										first=remain[:remain.find(' or ')]
										remain=remain[remain.find(' or ')+4:]
										if (first not in permissions) and first!='NONE':
											permissions.append(first)
										if remain.find(' or ')<0:
											ContainOr=0
											break
									if (remain not in permissions) and remain!='NONE':
										permissions.append(remain)
									continue

								if line.find('Intent')==0 and line.find('requires')>=0:
									temppermission=line[line.find('requires')+9:]
									if  temppermission.find(' or ') <0:
										ContainOr=0
										if (temppermission not in permissions) and temppermission!='NONE':
											permissions.append(temppermission)
										continue
									first='XXXX'
									remain=temppermission
									while ContainOr==1:
										first=remain[:remain.find(' or ')]
										remain=remain[remain.find(' or ')+4:]
										if (first not in permissions) and first != 'NONE':
											permissions.append(first)
										if remain.find(' or ')<0:
											ContainOr=0
											break
									if (remain not in permissions) and remain != 'NONE':
										permissions.append(remain)
									continue	

							if line.find("Do you think the results here are wrong?")>=0:
								maindict[packagename]=permissions
								OVERPRIVFDETECTED=0
								PERMISSIONSDETECTED=0
								packagename=''
								overprivs=[]
								permissions=[]
								continue

					finally:
						file_object.close()

		print json.dumps(maindict)
		#for (k,v) in maindict.iteritems():
			#print k + ":" 
			#print v
		print "number of packages: " + "%s"%packagenum
		print "number of non-overprivilage packages: " + "%s"%nonoverprivnum
		print "number of overprivilage packages: " + "%s"%overprivnum
		if packagenum != (overprivnum + nonoverprivnum):
			print "Errors in parsing"
		
					

if __name__=="__main__":
	exactpermissionparser=ExactPermissionParser("")
	#parse all the result files based on Stowaway in this root, make sure to change it bufore use
	exactpermissionparser.GetExactPerm("/home/zyqu/Research/Android_sec/parsexml/semant/stowawayresults/")


