#!/usr/bin/python

#Zhengyang Qu,
#Department of EECS, Northwestern University
#11/25/2011
#depack all the .apk files


import os

class Depack:
  def __init__(self,sourcepath,sinkpath):
    self.sourcepath=sourcepath
    self.sinkpath=sinkpath


    pass
    
  def depackage(self): 
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
        command="apktool d -f "+filepath+" "+self.sinkpath+'XXXXX'+f+'.apk'
	print command
        os.system(command)

  def getstringsmali(self,path):
    maindict={}
    list_dirs=os.walk(path)
    for root, dirs, files in list_dirs:
	for d in dirs:
		if d.find('XXXXX')>=0 and d.find('.apk')>=0:
			appname=d[d.find('XXXXX')+len('XXXXX'):]
			stringlist=[]			
			list_dirs_level2=os.walk(path+d)
			for rs, ds, fs in list_dirs_level2:
				for f in fs:
					
					sufix = os.path.splitext(f)[1][1:]
					if sufix == 'smali':
						file_obj=open(os.path.join(rs,f))
						try:
							alllines = file_obj.readlines()
							for line in alllines:
								if line.find('const-string')>=0:
									line=line.strip()
									line=line[line.find("\"")+1:]
									line=line[:line.find("\"")]
									line=line.replace('\\n','')
									line=line.replace('\\t','')
									line=line.replace("\\'","")
									line=line.replace('\\"','')
									line=line.replace('*','')
									line=line.replace('#','')
									line=line.replace('\\','')
									line=line.replace(',','')
									line=line.replace('.','')
									line=line.strip()
								        #flag=False
									#for char in line:
										#if char.isalpha():
											#flag=True
									if len(line)>0 and line.isalpha():#flag==True:
										#print line
										stringlist.append(line.lower())
						except:
							print "Errors in openning: "+os.path.join(rs,f)
						finally:
							file_obj.close()
			if len(appname)>0 and len(stringlist)>0 and (appname not in maindict):			
				maindict[appname]=stringlist

    print maindict
    file_op=open("StringtoAppend.txt",'w')
    try:
	for k in maindict:
		file_op.write(k+'\n')
		for v in maindict[k]:
			file_op.write(v+'\n')
		file_op.write('\n')
    except:
	print "Errors in writing file StringtoAppend.txt"
    finally:
	file_op.close()  

if __name__=="__main__":
  dep=Depack("/home/zyqu/Research/Android_sec/parsexml/semant/apps/","/home/zyqu/Research/Android_sec/parsexml/semant/depackedapps/")
  dep.depackage()
  dep.getstringsmali("/home/zyqu/Research/Android_sec/parsexml/semant/depackedapps/")
