#!/usr/bin/python

##Zhengyang Qu, EECS, Northwestern Univeristy, 02/17/2013##

import os
import json 
class FileParseUrl: 

	def __init__(self,path):
		self.path=path

	def GetUrl(self,path):
		maindict = {}
		list_dirs = os.walk(path) 
		packagenamenum=0
		descriptionnum=0
		for root, dirs, files in list_dirs: 
			for f in files:
				httplist=[]
				filepath=os.path.join(root, f)
				if filepath.find("meta")>=0:
					file_object=open(filepath)
					try:
						alllines = file_object.readlines()
						for line in alllines:
							if line.find("description:")>=0:
								line=line.strip()
								line = line[len("description:\"")+1: ]
								desc = line[: len(line)-1]
								descriptionnum=descriptionnum+1
							if line.find("packageName:")>=0: 
								line=line.strip()
								line = line[len("packageName:\"")+1: ]
								package = line[: len(line)-1]
								if package not in maindict:
									packagenamenum=packagenamenum+1
							if packagenamenum == descriptionnum and packagenamenum>0:
								maindict[package]=desc
					finally:
						file_object.close()

		print json.dumps(maindict)
		#for (k,v) in maindict.iteritems():
			#print k + ":\n" + v +"\n"
		print "number of packages: " + "%s"%packagenamenum
		print "number of descriptions: "+ "%s"%descriptionnum
		
					

if __name__=="__main__":
	fileparseurl=FileParseUrl("")
	#parse all the meta files in this root, make sure to change it bufore use
	fileparseurl.GetUrl("/home/zyqu/Research/Android_sec/parsexml/semant/metafiles/")


