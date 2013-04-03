#!/usr/bin/python

#Zhengyang Qu,
#Department of EECS, Northwestern University
#11/25/2011
#depack all the .apk files


import os,time

class ExtractedFromZip:
  def __init__(self,sourcepath,sinkpath):
    self.sourcepath=sourcepath
    self.sinkpath=sinkpath
    pass
    
  def extract(self): 
    list_dirs=os.walk(self.sourcepath)
    command="rm -rf " + self.sinkpath
    os.system(command)
    command="mkdir " + self.sinkpath
    os.system(command)
    #command="mkdir " + self.sinkpath+'/test'
    #os.system(command)
    for root, dirs, files in list_dirs:
      for f in files: 
        filepath=os.path.join(root, f)
	appname=os.path.basename(filepath)
        command='unzip '+filepath+' -d '+self.sinkpath+'XXXXX'+appname
        os.system(command)


  def dedex(self,path,dedexpath):
    javapath='/home/zyqu/Research/Android_sec/jdk1.7.0_17/bin/'

    list_dirs=os.walk(path)
    for root, dirs, files in list_dirs:
	for d in dirs:
		if d.find('XXXXX')>=0 and d.find('.apk')>=0:
			appname=d[d.find('XXXXX')+len('XXXXX'):]
			list_dirs_level2=os.walk(path+d)
			for rs, ds, fs in list_dirs_level2:
				for f in fs:
					if f.find('classes.dex')>=0:
						fullpath=os.path.join(path,d)
						fullpath=os.path.join(fullpath,f)
						command=javapath+'java -cp .:'+javapath+' -jar ddx1.26.jar -d '+dedexpath+'XXXXX'+appname+'/ '+fullpath
						os.system(command)





  def analysis(self,path): 
    maindict={}
    numoffiles={}
    numofdirs={}
    list_dirs=os.walk(path)
    for root, dirs, files in list_dirs:
	for d in dirs:
		if d.find('XXXXX')>=0 and d.find('.apk')>=0:
			typedict={}
			appname=d[d.find('XXXXX')+len('XXXXX'):]
			list_dirs_level2=os.walk(path+d)
			dircount=0
			for rs, ds, fs in list_dirs_level2:
				if len(ds)>0:
					dircount=dircount+len(ds)
				for f in fs:
					sufix = os.path.splitext(f)[1][1:]
					if sufix not in typedict:
						typedict[sufix]=1
						continue
					elif sufix in typedict:
						typedict[sufix]=typedict[sufix]+1
			if appname not in maindict:			
				maindict[appname]=typedict
			count=0
			for elem in typedict:
				count=count+typedict[elem]
			if appname not in numoffiles:
				numoffiles[appname]=count
				#count=0
			if appname not in numofdirs:
				numofdirs[appname]=dircount
				#dircount=0
			
    #print maindict
    file_op1=open('typecount.txt','w')
    try:
	for k in maindict:
		file_op1.write(k+'\n')
		for v in maindict[k]:
			file_op1.write(v+": %s\n"%maindict[k][v])
		file_op1.write('\n')	
    except:
	print "Errors in writing file typecount.txt"
    finally:
	file_op1.close()

    file_op2=open('filecount.txt','w')
    try:
	for k in numoffiles:
		file_op2.write(k+'\n')
		file_op2.write('%s\n\n'%numoffiles[k])
    except:
	print "Errors in writing file filecount.txt"
    finally:
	file_op2.close()

    file_op3=open('dircount.txt','w')
    try:
	for k in numofdirs:
		file_op3.write(k+'\n')
		file_op3.write('%s\n\n'%numofdirs[k])
    except:
	print "Errors in writing file dircount.txt"
    finally:
	file_op3.close()
    return maindict



if __name__=="__main__":
  dedexpath='/home/zyqu/Research/Android_sec/parsexml/semant/dedexedapps/'
  dep=ExtractedFromZip("/home/zyqu/Research/Android_sec/parsexml/semant/apps/","/home/zyqu/Research/Android_sec/parsexml/semant/extractedapps/")
  dep.extract()
  dep.analysis(dep.sinkpath)
  #dep.dedex(dep.sinkpath,dedexpath)

