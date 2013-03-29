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
		desc=''
		package=''

		i=0
		j=0
		k=0
		speclist=[]
		while i<10:
			while j<10:
				while k<10:
					speclist.append('\\'+'%s'%i+'%s'%j+'%s'%k)
					k=k+1
				k=0
				j=j+1				
			j=0
			i=i+1
		


		for root, dirs, files in list_dirs: 
			for f in files:
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
								for eachspecwd in speclist:
									desc=desc.replace(eachspecwd,'')
								desc=desc.replace('\\n',' ')
								desc=desc.replace('\\t',' ')
								desc=desc.replace("\\'","\'")
								desc=desc.replace('\\"','\"')
								desc=desc.replace('*','')
								desc=desc.replace('#','')
								desc=desc.replace('\\',' ')
								desc=desc.strip()
								descriptionnum=descriptionnum+1
								continue

							if line.find("promoText:")>=0:
								line=line.strip()
								line = line[len("promoText:\"")+1: ]
								desc = desc + ' '+line[: len(line)-1]
								for eachspecwd in speclist:
									desc=desc.replace(eachspecwd,'')
								desc=desc.replace('\\n',' ')
								desc=desc.replace('\\t',' ')
								desc=desc.replace("\\'","\'")
								desc=desc.replace('\\"','\"')
								desc=desc.replace('*','')
								desc=desc.replace('#','')
								desc=desc.replace('\\',' ')
								desc=desc.strip()
								continue

							if line.find("recentChanges:")>=0:
								line=line.strip()
								line = line[len("recentChanges:\"")+1: ]
								recentchange =  line[: len(line)-1]
								for eachspecwd in speclist:
									recentchange=recentchange.replace(eachspecwd,'')
								recentchange=recentchange.replace('\\n',' ')
								recentchange=recentchange.replace('\\t',' ')
								recentchange=recentchange.replace("\\'","\'")
								recentchange=recentchange.replace('\\"','\"')
								recentchange=recentchange.replace('*','')
								recentchange=recentchange.replace('#','')
								recentchange=recentchange.replace('\\',' ')
								recentchange=recentchange.replace('fixed','')
								recentchange=recentchange.replace('Fixed','')
								recentchange=recentchange.replace('fix','')
								recentchange=recentchange.replace('Fix','')
								recentchange=recentchange.replace('bugs','')
								recentchange=recentchange.replace('Bugs','')
								recentchange=recentchange.replace('bug','')
								recentchange=recentchange.replace('Bug','')
								desc=desc+recentchange.strip()
								continue


							if line.find("packageName:")>=0: 
								line=line.strip()
								line = line[len("packageName:\"")+1: ]
								package = line[: len(line)-1]
								if package not in maindict:
									packagenamenum=packagenamenum+1
									continue

							if packagenamenum == descriptionnum and packagenamenum>0:
								maindict[package]=desc

					finally:
						file_object.close()

		#print json.dumps(maindict)

		file_op=open('descwithapk.txt',"w")
		try:
			for k in maindict:
				file_op.write(k+'.apk\n')
				file_op.write(maindict[k]+'\n')
				file_op.write('\n')
				file_op.flush()
		except:
			print "Errors in writing the file keyworddictory.txt"
		finally:
			file_op.close()
		print "number of packages: " + "%s"%packagenamenum
		print "number of descriptions: "+ "%s"%descriptionnum
		
					

if __name__=="__main__":
	fileparseurl=FileParseUrl("")
	#parse all the meta files in this root, make sure to change it bufore use
	fileparseurl.GetUrl("/home/zyqu/Research/Android_sec/parsexml/semant/metafiles/")


