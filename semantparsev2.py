#!/usr/bin/python

#2/4/2013 Zhengyang 

import os,time
from xml.dom.minidom import parse,parseString
import xml.etree.ElementTree

#get the least subset of each category of apps, e.g. social networks
fullpermission = {
'android.permission.ACCESS_CHECKIN_PROPERTIES' : '1',
'android.permission.ACCESS_COARSE_LOCATION' : '2',
'android.permission.ACCESS_FINE_LOCATION' : '3',
'android.permission.ACCESS_LOCATION_EXTRA_COMMANDS' : '4',
'android.permission.ACCESS_MOCK_LOCATION' : '5',
'android.permission.ACCESS_NETWORK_STATE' : '6',
'android.permission.ACCESS_SURFACE_FLINGER' : '7',
'android.permission.ACCESS_WIFI_STATE' : '8',
'android.permission.ACCOUNT_MANAGER' : '9',
'android.permission.ADD_VOICEMAIL' : '10',
'android.permission.AUTHENTICATE_ACCOUNTS' : '11',
'android.permission.BATTERY_STATS' : '12',
'android.permission.BIND_ACCESSIBILITY_SERVICE' : '13',
'android.permission.BIND_APPWIDGET' : '14',
'android.permission.BIND_DEVICE_ADMIN' : '15',
'android.permission.BIND_INPUT_METHOD' : '16',
'android.permission.BIND_REMOTEVIEWS' : '17',
'android.permission.BIND_TEXT_SERVICE' : '18',
'android.permission.BIND_VPN_SERVICE' : '19',
'android.permission.BIND_WALLPAPER' : '20',
'android.permission.BLUETOOTH' : '21',
'android.permission.BLUETOOTH_ADMIN' : '22',
'android.permission.BRICK' : '23',
'android.permission.BROADCAST_PACKAGE_REMOVED' : '24',
'android.permission.BROADCAST_SMS' : '25',
'android.permission.BROADCAST_STICKY' : '26',
'android.permission.BROADCAST_WAP_PUSH' : '27',
'android.permission.CALL_PHONE' : '28',
'android.permission.CALL_PRIVILEGED' : '29',
'android.permission.CAMERA' : '30',
'android.permission.CHANGE_COMPONENT_ENABLED_STATE' : '31',
'android.permission.CHANGE_CONFIGURATION' : '32',
'android.permission.CHANGE_NETWORK_STATE' : '33',
'android.permission.CHANGE_WIFI_MULTICAST_STATE' : '34',
'android.permission.CHANGE_WIFI_STATE' : '35',
'android.permission.CLEAR_APP_CACHE' : '36',
'android.permission.CLEAR_APP_USER_DATA' : '37',
'android.permission.CONTROL_LOCATION_UPDATES' : '38',
'android.permission.DELETE_CACHE_FILES' : '39',
'android.permission.DELETE_PACKAGES' : '40',
'android.permission.DEVICE_POWER' : '41',
'android.permission.DIAGNOSTIC' : '42',
'android.permission.DISABLE_KEYGUARD' : '43',
'android.permission.DUMP' : '44',
'android.permission.EXPAND_STATUS_BAR' : '45',
'android.permission.FACTORY_TEST' : '46',
'android.permission.FLASHLIGHT' : '47',
'android.permission.FORCE_BACK' : '48',
'android.permission.GET_ACCOUNTS' : '49',
'android.permission.GET_PACKAGE_SIZE' : '50',
'android.permission.GET_TASKS' : '51',
'android.permission.GLOBAL_SEARCH' : '52',
'android.permission.HARDWARE_TEST' : '53',
'android.permission.INJECT_EVENTS' : '54',
'android.permission.INSTALL_LOCATION_PROVIDER' : '55',
'android.permission.INSTALL_PACKAGES' : '56',
'android.permission.INTERNAL_SYSTEM_WINDOW' : '57',
'android.permission.INTERNET' : '58',
'android.permission.KILL_BACKGROUND_PROCESSES' : '59',
'android.permission.MANAGE_ACCOUNTS' : '60',
'android.permission.MANAGE_APP_TOKENS' : '61',
'android.permission.MASTER_CLEAR' : '62',
'android.permission.MODIFY_AUDIO_SETTINGS' : '63',
'android.permission.MODIFY_PHONE_STATE' : '64',
'android.permission.MOUNT_FORMAT_FILESYSTEMS' : '65',
'android.permission.MOUNT_UNMOUNT_FILESYSTEMS' : '66',
'android.permission.NFC' : '67',
'android.permission.PERSISTENT_ACTIVITY' : '68',
'android.permission.PROCESS_OUTGOING_CALLS' : '69',
'android.permission.READ_CALENDAR' : '70',
'android.permission.READ_CALL_LOG' : '71',
'android.permission.READ_CONTACTS' : '72',
'android.permission.READ_EXTERNAL_STORAGE' : '73',
'android.permission.READ_FRAME_BUFFER' : '74',
'android.permission.READ_HISTORY_BOOKMARKS' : '75',
'android.permission.READ_INPUT_STATE' : '76',
'android.permission.READ_LOGS' : '77',
'android.permission.READ_PHONE_STATE' : '78',
'android.permission.READ_PROFILE' : '79',
'android.permission.READ_SMS' : '80',
'android.permission.READ_SOCIAL_STREAM' : '81',
'android.permission.READ_SYNC_SETTINGS' : '82',
'android.permission.READ_SYNC_STATS' : '83',
'android.permission.READ_USER_DICTIONARY' : '84',
'android.permission.REBOOT' : '85',
'android.permission.RECEIVE_BOOT_COMPLETED' : '86',
'android.permission.RECEIVE_MMS' : '87',
'android.permission.RECEIVE_SMS' : '88',
'android.permission.RECEIVE_WAP_PUSH' : '89',
'android.permission.RECORD_AUDIO' : '90',
'android.permission.REORDER_TASKS' : '91',
'android.permission.RESTART_PACKAGES' : '92',
'android.permission.SEND_SMS' : '93',
'android.permission.SET_ACTIVITY_WATCHER' : '94',
'android.permission.SET_ALARM' : '95',
'android.permission.SET_ALWAYS_FINISH' : '96',
'android.permission.SET_ANIMATION_SCALE' : '97',
'android.permission.SET_DEBUG_APP' : '98',
'android.permission.SET_ORIENTATION' : '99',
'android.permission.SET_POINTER_SPEED' : '100',
'android.permission.SET_PREFERRED_APPLICATIONS' : '101',
'android.permission.SET_PROCESS_LIMIT' : '102',
'android.permission.SET_TIME' : '103',
'android.permission.SET_TIME_ZONE' : '104',
'android.permission.SET_WALLPAPER' : '105',
'android.permission.SET_WALLPAPER_HINTS' : '106',
'android.permission.SIGNAL_PERSISTENT_PROCESSES' : '107',
'android.permission.STATUS_BAR' : '108',
'android.permission.SUBSCRIBED_FEEDS_READ' : '109',
'android.permission.SUBSCRIBED_FEEDS_WRITE' : '110',
'android.permission.SYSTEM_ALERT_WINDOW' : '111',
'android.permission.UPDATE_DEVICE_STATS' : '112',
'android.permission.USE_CREDENTIALS' : '113',
'android.permission.USE_SIP' : '114',
'android.permission.VIBRATE' : '115',
'android.permission.WAKE_LOCK' : '116',
'android.permission.WRITE_APN_SETTINGS' : '117',
'android.permission.WRITE_CALENDAR' : '118',
'android.permission.WRITE_CALL_LOG' : '119',
'android.permission.WRITE_CONTACTS' : '120',
'android.permission.WRITE_EXTERNAL_STORAGE' : '121',
'android.permission.WRITE_GSERVICES' : '122',
'android.permission.WRITE_HISTORY_BOOKMARKS' : '123',
'android.permission.WRITE_PROFILE' : '124',
'android.permission.WRITE_SECURE_SETTINGS' : '125',
'android.permission.WRITE_SETTINGS' : '126',
'android.permission.WRITE_SMS' : '127',
'android.permission.WRITE_SOCIAL_STREAM' : '128',
'android.permission.WRITE_SYNC_SETTINGS' : '129',
'android.permission.WRITE_USER_DICTIONARY' : '130'
}

fullpermission0 = dict()
for (k,v) in fullpermission.iteritems():
    fullpermission0 [k.lower()] = v

class XmlConfig: 
      def __init__(self,path):    
         self.path=path
	 self.count=0
	 self.currentpermission=dict()
         self.file_output=open("/home/zyqu/Research/Android_sec/parsexml/semant/permissionsofapp","w")

      def GetAndroidManifestXml(self,path): 
         doc=parse(path)
	 usespermissions=[]
	 tempcurrentpermission=dict()
#get the package full name
	 for node in doc.getElementsByTagName("manifest"):
                 package=node.getAttribute("package")
	 #print "analyzing" + package
#get the required permission
	 for node in doc.getElementsByTagName("uses-permission"):
                 name=node.getAttribute("android:name")
		 tempname=name.lower()
		 if 'android.permission' in tempname:
                 	if name.startswith('.'):
                 		name = package + name
                	elif '.' not in name:
                 		name = package + "." + name
		 	name=name.lower()
			if name in fullpermission0:
		 		usespermissions.append(name)
	 if len(usespermissions) != 0:
	 	 #print "No permissions: " + package
	 	 if self.count==1:
		 	for elem in usespermissions:
				self.currentpermission[elem]=fullpermission0[elem]
		 	tempcurrentpermission=self.currentpermission
	 	 elif self.count > 1:
		 	for (k,v) in self.currentpermission.iteritems():
		 		 if k in usespermissions:
		 		 	tempcurrentpermission[k]=v

	 	 self.count=self.count+1
	 	 self.currentpermission=tempcurrentpermission
		 outstr=package
		 for elem in usespermissions:
			outstr=outstr+'	'+fullpermission0[elem]
		 self.file_output.write(outstr+'\n')       
	 #print self.currentpermission
	 #print usespermissions

if __name__=="__main__":
    xmlf=XmlConfig("")
    operationtime=[]
    #where we should put the fold of apps classified
    rootDir="/home/zyqu/Research/Android_sec/parsexml/semant/android_apps/businessdepackedapps/"
    list_dirs = os.walk(rootDir) 
    for root, dirs, files in list_dirs:     
        for f in files: 
            filepath=os.path.join(root, f)
	    if filepath.find("AndroidManifest.xml")>=0 and filepath.find("AndroidManifest.xml~")<0:
	      #print filepath
              starttime=time.time()
	      xmlf.GetAndroidManifestXml(filepath)
              endtime=time.time()
              interval=endtime-starttime
              operationtime.append(interval)	      
    print xmlf.currentpermission
    print xmlf.count
    xmlf.file_output.close()
    manifestanalyze=open("/home/zyqu/Research/Android_sec/parsexml/semant/securityinfoextractiontime","w")
    try:
      for elem in operationtime:
        outstr = "%s"%elem
        manifestanalyze.write(outstr)
        manifestanalyze.write(', ')
    finally:
      manifestanalyze.close()  





