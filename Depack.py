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

    operationtime=[]
    rootDir=self.sourcepath
    list_dirs=os.walk(rootDir)
    command="rm -rf " + self.sinkpath
    os.system(command)
    command="mkdir " + self.sinkpath
    os.system(command)
    for root, dirs, files in list_dirs:
      for f in files: 
        filepath=os.path.join(root, f)
        f=f[:len(f)-4]
        command="apktool d -f "+filepath+" "+self.sinkpath+f
        starttime=time.time()
        os.system(command)
        endtime=time.time()
        interval=endtime-starttime
	operationtime.append(interval)
        print operationtime

    file_output=open("/home/zyqu/Research/Android_sec/parsexml/semant/depacktime","w")
    try:
      for elem in operationtime:
        outstr = "%s"%elem
        file_output.write(outstr)
        file_output.write(', ')

    finally:
      file_output.close()   




if __name__=="__main__":
  dep=Depack("/home/zyqu/Research/Android_sec/parsexml/semant/android_apps/entertainmentappsFeb13","/home/zyqu/Research/Android_sec/parsexml/semant/android_apps/entertainmentdepackedapps/")
  dep.depackage()
