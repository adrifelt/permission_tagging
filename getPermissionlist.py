#!/usr/bin/python


class PermissionList: 

	def __init__(self,path):
		self.path=path

	def GetList(self,path):
		file_object=open(path)
		try:
			list_of_all_the_lines = file_object.readlines()
			count=1
			for line in list_of_all_the_lines:
				line=line.strip()
				print '\'android.permission.'+line+'\' : \''+ '%s'%count +'\','
				count=count+1
		finally:
			file_object.close()
	
if __name__=="__main__":
	permissionlist=PermissionList("")
	permissionlist.GetList("/home/zyqu/Research/Android_sec/parsexml/semant/full_permission_list")

