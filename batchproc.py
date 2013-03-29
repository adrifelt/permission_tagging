#!/usr/bin/python

#Zhengyang Qu,
#Department of EECS, Northwestern University
#11/25/2011
#depack all the .apk files

import os,time

class Depack:
  def __init__(self,sourcepath,sinkpath):
    self.sourcepath=sourcepath
    self.sinkpath=sinkpath
    pass
    
  def depackage(self): 

    rootDir=self.sourcepath
    list_dirs=os.walk(rootDir)
    count=0
    for root, dirs, files in list_dirs:
      for f in files: 
        filepath=os.path.join(root, f)
	if filepath.find('.apk')>=0:
		name=os.path.basename(filepath)
		os.chdir('/home/peng/Stowaway-1.2.4')
		command='./stowaway.sh ~/apps/'+name+' ~/res/'+name+' 1>temp'
        	os.system(command)
		command='rm -r /home/peng/res/'+name+'/baksmali'
            	os.system(command)
        	command='rm -r /home/peng/res/'+name+'/dedex'
            	os.system(command)
        	command='rm -r /home/peng/res/'+name+'/IntentResults'
            	os.system(command)
        	command='rm -r /home/peng/res/'+name+'/log'
            	os.system(command)
        	command='rm -r /home/peng/res/'+name+'/ProviderResults'
            	os.system(command)
        	command='rm -r /home/peng/res/'+name+'/ReflectionResults'
            	os.system(command)
        	command='rm -r /home/peng/res/'+name+'/unzip'
            	os.system(command)
		count=count+1
		print count





if __name__=="__main__":
  dep=Depack("/home/peng/apps/","/home/peng/res/")
  dep.depackage()
