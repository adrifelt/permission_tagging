#!/bin/bash

REFLECTIONONLY=false

LOC=$1

#############################################################################
# Make sure that permissions are set up correctly
#############################################################################

chmod u+x *.rb
chmod u+x *.py

#############################################################################
# SPECIAL CASE: ACCORDING TO ARGS, FIRST TIME THIS HAS BEEN RUN
#############################################################################

if [ -z $1 ]
then
	echo "Correct usage: stowaway.sh [path to apk].apk [path to output]"
	echo "Or: stowaway.sh [path to folder with /unzip, /dedex, AndroidManifest.xml]"
	exit
elif [ ${1: -4} == ".apk" ]
then
	if [ -z $2 ]
	then
		echo "Correct usage: [path to apk].apk [path to output]"
		echo "You forgot the path to output."
		echo "I need to know where to put the results."
		exit
	elif [ ! -d "$2"/dedex ]
	then
	    mkdir $2
		#echo "Unpacking "$1
		unzip $1 -d $2/unzip/
		
		#echo "Disassembling the APK file"
	    mkdir $2/dedex
	    java -jar ddx1.14.jar -o -D -r -d $2/dedex/ $2/unzip/classes.dex
		rm -rf $2/unzip/classes.dex
		rm -rf $2/dedex/dex.log
		
		echo "Getting the XML files"
		if [ -d out ]
		then
			rm -rf out
		fi
		./apktool d -s $1 $2/baksmali
		cp $2/baksmali/AndroidManifest.xml $2/AndroidManifest.xml
		rm $2/baksmali/classes.dex
		rm $2/baksmali/apktool.yml

		LOC=$2
	fi
elif [ ! -d "$1"/dedex ]
then
	echo "Correct usage: stowaway.sh [path to apk].apk [path to output]"
	echo "Or: stowaway.sh [path to folder with /unzip, /dedex, AndroidManifest.xml]"
	exit
fi

#############################################################################
# PLAIN API CALLS
#############################################################################

find $LOC -name "*.ddx" > $LOC/dedex/DDXFILELIST

if [ $REFLECTIONONLY = false ]; then
	if [ ! -d $LOC/log ]
	then
		mkdir $LOC/log
	fi

	# Getting the main API list
	./get_apis.rb $LOC/dedex/DDXFILELIST > $LOC/tmp 
	sed 's/\//\./g' $LOC/tmp > $LOC/plainapicalls.txt 
fi

# Moving the plain API list to apicalls.txt
sort -u $LOC/plainapicalls.txt > $LOC/apicalls.txt

#############################################################################
# REFLECTION ANALYSIS
#############################################################################

if [ ! -d $LOC/ReflectionResults ]
then
	mkdir $LOC/ReflectionResults/
fi
./reflectionanalysis.rb $LOC/dedex/ $LOC/ReflectionResults/ > $LOC/log/reflection.log
cat $LOC/ReflectionResults/MethodOrConsUse.txt >> $LOC/ReflectionResults/reflectivecalls.txt
sort -u $LOC/ReflectionResults/reflectivecalls.txt >> $LOC/apicalls.txt
./getclasscalls.rb $LOC/dedex/DDXFILELIST > $LOC/ReflectionResults/getclasses.txt
sort -u $LOC/ReflectionResults/getclasses.txt > $LOC/tmp2
sed 's/\//\./g' $LOC/tmp2 >> $LOC/ReflectionResults/forNameUse.txt
sort -u $LOC/ReflectionResults/forNameUse.txt > $LOC/tmp2
mv $LOC/tmp2 $LOC/ReflectionResults/forNameUse.txt
./reflectionsHack.py $LOC/ReflectionResults/forNameUse.txt $LOC/ReflectionResults/reflectiveDebug.txt > $LOC/ReflectionResults/hack.txt
sort -u $LOC/ReflectionResults/hack.txt >> $LOC/apicalls.txt
./removepackages.py $LOC/ReflectionResults/reflectiveDebugSinkFailures.txt > $LOC/ReflectionResults/reflectiveDebugSink-nopackages.txt
./removeirrelevant.py $LOC/ReflectionResults/reflectiveDebugSink-nopackages.txt > $LOC/ReflectionResults/reflectiveDebugSink-noirrelevant.txt

#############################################################################
# UNKNOWN API CALLS
#############################################################################

if [ $REFLECTIONONLY = false ]; then
	calls=$(cat $LOC/apicalls.txt)  
	if [ -e $LOC/uncovered.txt ] 
	then 
		rm $LOC/uncovered.txt 
		touch $LOC/uncovered.txt 
	fi 
	if [ -e $LOC/unknown.txt ]
	then
		rm $LOC/unknown.txt 
		touch $LOC/unknown.txt
	fi
	for call in $calls 
	do
		if grep -qF $call"(" uncovered.txt
		then
			echo $call >> $LOC/uncovered.txt
		fi
		if grep -qF $call"(" allmethods.txt
		then
			:
		else
			echo $call >> $LOC/unknown.txt
		fi
	done
fi

#############################################################################
# ATTRIBUTING PERMISSIONS TO API CALLS
#############################################################################

java ManifestGeneration $LOC/apicalls.txt permissionmap.csv > $LOC/OurPermissions 2>$LOC/sources

#############################################################################
# INTENT ANALYSIS
#############################################################################

if [ $REFLECTIONONLY = false ]; then
	if [ ! -d $LOC/IntentResults ]  
	then
		mkdir $LOC/IntentResults/
	fi
	./recvActionManifestAnalysis.rb $LOC/AndroidManifest.xml $LOC/IntentResults/  
	./sendActionIntentAnalysis.rb -sdv $LOC $LOC/dedex $LOC/AndroidManifest.xml $LOC/IntentResults >$LOC/log/intent-send.log  

	# Identify disallowed broadcasts
	DISALLOWEDBROADCASTS=$(cat DisallowedBroadcasts.txt)
	for B in $DISALLOWEDBROADCASTS
	do
		if grep -qi $B $LOC/IntentResults/sendBroadcastActions.txt
		then
			echo "This application tries to send disallowed broadcast "$B
		fi
	done
fi

# Permissions needed to send broadcasts
checkBroadcasts() {
	if grep -qi "android.app.action.DEVICE_ADMIN_ENABLED" $1
	then
		echo "android.permission.BIND_DEVICE_ADMIN" >> $2
		echo "Intent android.app.action.DEVICE_BIND_ENABLED requires android.permission.BIND_DEVICE_ADMIN" >> $3
	fi
	if grep -qi "android.intent.action.EXTERNAL_APPLICATIONS_UNAVAILABLE" $1
	then
		echo "android.permission.BROADCAST_PACKAGE_REMOVED" >> $2
		echo "Intent android.intent.action.EXTERNAL_APPLICATIONS_UNAVAILABLE requires android.permission.BROADCAST_PACKAGE_REMOVED" >> $3
	fi
	if grep -qi "android.intent.action.PACKAGE_CHANGED" $1
	then
		echo "android.permission.BROADCAST_PACKAGE_REMOVED" >> $2
		echo "Intent android.intent.action.PACKAGE_CHANGED requires android.permission.BROADCAST_PACKAGE_REMOVED" >> $3
	fi
	if grep -qi "android.intent.action.PACKAGE_REMOVED" $1
	then
		echo "android.permission.BROADCAST_PACKAGE_REMOVED" >> $2
		echo "Intent android.intent.action.PACKAGE_REMOVED requires android.permission.BROADCAST_PACKAGE_REMOVED" >> $3
	fi
	if grep -qi "android.intent.action.UID_REMOVED" $1
	then
		echo "android.permission.BROADCAST_PACKAGE_REMOVED" >> $2
		echo "Intent android.intent.action.UID_REMOVED requires android.permission.BROADCAST_PACKAGE_REMOVED" >> $3
	fi
	if grep -qi "android.provider.Telephony.SMS_RECEIVED" $1
	then
		echo "android.permission.BROADCAST_SMS" >> $2
		echo "Intent android.provider.Telephony.SMS_RECEIVED requires android.permission.SMS_RECEIVED" >> $3
	fi
}

# Permissions needed to start activities
checkActivities() {
	if grep -qi "android.bluetooth.adapter.action.REQUEST_DISCOVERABLE" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.adapter.action.REQUEST_DISCOVERABLE requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.bluetooth.adapter.action.REQUEST_ENABLE" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.adapter.action.REQUEST_ENABLE requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.intent.action.CALL" $1
	then
		echo "android.permission.CALL_PHONE" >> $2
		echo "Intent android.intent.action.CALL requires android.permission.CALL_PHONE" >> $3
	fi
	if grep -qi "android.intent.action.CALL_PRIVILEGED" $1
	then
		echo "android.permission.CALL_PRIVILEGED" >> $2
		echo "Intent android.intent.action.CALL_PRIVILEGED requires android.permission.CALL_PRIVILEGED" >> $3
	fi
	if grep -qi "android.intent.action.CALL_EMERGENCY" $1
	then
		echo "android.permission.CALL_PRIVILEGED" >> $2
		echo "Intent android.intent.action.CALL_EMERGENCY requires android.permission.CALL_PRIVILEGED" >> $3
	fi
	if grep -qi "android.search.action.GLOBAL_SEARCH" $1
	then
		echo "android.permission.GLOBAL_SEARCH_CONTROL" >> $2
		echo "Intent android.search.action.GLOBAL_SEARCH requires android.permission.GLOBAL_SEARCH_CONTROL" >> $3
	fi
	if grep -qi "android.intent.action.ACTION_REQUEST_SHUTDOWN" $1
	then
		echo "android.permission.SHUTDOWN" >> $2
		echo "Intent android.intent.action.ACTION_REQUEST_SHUTDOWN requires android.permission.SHUTDOWN" >> $3
	fi
}

# Permissions needed to start services
checkServices() {
	if grep -q "android.view.InputMethod" $1
	then
		echo "android.permission.BIND_INPUT_METHOD" >> $2
		echo "Intent android.view.InputMethod requires android.permission.BIND_INPUT_METHOD" >> $3
	fi
	if grep -q "android.service.wallpaper.WallpaperService" $1
	then
		echo "android.permission.BIND_WALLPAPER" >> $2
		echo "Intent android.service.wallpaper.WallpaperService requires android.permission.BIND_WALLPAPER" >> $3
	fi
}

# Permissions needed to RECEIVE intents (broadcasts)
checkReceivers() {
	if grep -qi "android.provider.Telephony.SMS_RECEIVED" $1
	then
		echo "android.permission.RECEIVE_SMS" >> $2
		echo "Intent android.provider.Telephony.SMS_RECEIVED requires android.permission.RECEIVE_SMS" >> $3
	fi
	if grep -qi "android.provider.Telephony.SIM_FULL" $1
	then
		echo "android.permission.RECEIVE_SMS" >> $2
		echo "Intent android.provider.Telephony.SIM_FULL requires android.permission.RECEIVE_SMS" >> $3
	fi
	if grep -qi "android.provider.Telephony.WAP_PUSH_RECEIVED" $1
	then
		echo "android.permission.RECEIVE_MMS" >> $2
		echo "android.permission.RECEIVE_WAP_PUSH" >> $2
		echo "Intent android.provider.Telephony.WAP_PUSH_RECEIVED requires android.permission.RECEIVE_MMS and android.permission.RECEIVE_WAP_PUSH" >> $3
	fi
	if grep -qi "android.provider.Telephony.SMS_REJECTED" $1
	then
		echo "android.permission.RECEIVE_SMS" >> $2
		echo "Intent android.provider.Telephony.SMS_REJECTED requires android.permission.RECEIVE_SMS" >> $3
	fi
	if grep -qi "android.intent.action.NEW_OUTGOING_CALL" $1
	then
		echo "android.permission.PROCESS_OUTGOING_CALLS" >> $2
		echo "Intent android.intent.action.NEW_OUTGOING_CALL requires android.permission.PROCESS_OUTGOING_CALLS" >> $3
	fi
	if grep -qi "android.intent.action.BOOT_COMPLETED" $1
	then
		echo "android.permission.RECEIVE_BOOT_COMPLETED" >> $2
		echo "Intent android.intent.action.BOOT_COMPLETED requires android.permission.RECEIVE_BOOT_COMPLETED" >> $3
	fi
	if grep -qi "android.bluetooth.a2dp.action.SINK_STATE_CHANGED" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.a2dp.action.SINK_STATE_CHANGED requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.intent.action.PHONE_STATE" $1
	then
		echo "android.permission.READ_PHONE_STATE" >> $2
		echo "Intent android.intent.action.PHONE_STATE requires android.permission.READ_PHONE_STATE" >> $3
	fi
	if grep -qi "android.bluetooth.adapter.action.STATE_CHANGED" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.adapter.action.STATE_CHANGED requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.bluetooth.adapter.action.SCAN_MODE_CHANGED" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.adapter.action.SCAN_MODE_CHANGED requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.bluetooth.device.action.BOND_STATE_CHANGED" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.device.action.BOND_STATE_CHANGED requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.bluetooth.device.action.UUID" $1
	then
		echo "android.permission.BLUETOOTH_ADMIN" >> $2
		echo "Intent android.bluetooth.device.action.UUID requires android.permission.BLUETOOTH_ADMIN" >> $3
	fi
	if grep -qi "android.bluetooth.adapter.action.LOCAL_NAME_CHANGED" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.adapter.action.LOCAL_NAME_CHANGED requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.bluetooth.adapter.action.DISCOVERY_STARTED" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.adapter.action.DISCOVERY_STARTED requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.bluetooth.adapter.action.DISCOVERY_FINISHED" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.adapter.action.DISCOVERY_FINISHED requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.bluetooth.device.action.ACL_CONNECTED" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.device.action.ACL_CONNECTED requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.bluetooth.device.action.ACL_DISCONNECTED" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.device.action.ACL_DISCONNECTED requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.bluetooth.device.action.ACL_DISCONNECT_REQUESTED" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.device.action.ACL_DISCONNECT_REQUESTED requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.bluetooth.device.action.NAME_CHANGED" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.device.action.NAME_CHANGED requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.bluetooth.device.action.FOUND" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.device.action.FOUND requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.bluetooth.device.action.CLASS_CHANGED" $1
	then
		echo "android.permission.BLUETOOTH" >> $2
		echo "Intent android.bluetooth.device.action.CLASS_CHANGED requires android.permission.BLUETOOTH" >> $3
	fi
	if grep -qi "android.intent.action.DATA_SMS_RECEIVED" $1
	then
		echo "android.permission.RECEIVE_SMS" >> $2
		echo "Intent android.intent.action.DATA_SMS_RECEIVED requires android.permission.RECEIVE_SMS" >> $3
	fi
	if grep -qi "android.intent.action.NEW_OUTGOING_CALL" $1
	then
		echo "android.permission.PROCESS_OUTGOING_CALLS" >> $2
		echo "Intent android.intent.action.NEW_OUTGOING_CALL requires android.permission.PROCESS_OUTGOING_CALLS" >> $3
	fi
}

if [ $REFLECTIONONLY = false ]; then
	if [ -e $LOC/IntentResults/permissions.txt ]
	then
		rm $LOC/IntentResults/permissions.txt
	fi
	touch $LOC/IntentResults/permissions.txt
	
	checkBroadcasts $LOC/IntentResults/sendBroadcastActions.txt $LOC/IntentResults/permissions.txt $LOC/sources
	checkActivities $LOC/IntentResults/sendActivityActions.txt $LOC/IntentResults/permissions.txt $LOC/sources
	checkServices $LOC/IntentResults/sendServiceActions.txt $LOC/IntentResults/permissions.txt $LOC/sources
	checkReceivers $LOC/IntentResults/recvDynamicActions.txt $LOC/IntentResults/permissions.txt $LOC/sources
	checkReceivers $LOC/IntentResults/recvBroadcastActions.txt $LOC/IntentResults/permissions.txt $LOC/sources

	if [ -s sendOtherActions.txt ]
	then
		checkBroadcasts $LOC/IntentResults/sendOtherActions.txt $LOC/IntentResults/permissions.txt $LOC/sources
		checkActivities $LOC/IntentResults/sendOtherActions.txt $LOC/IntentResults/permissions.txt $LOC/sources
		checkServices $LOC/IntentResults/sendOtherActions.txt $LOC/IntentResults/permissions.txt $LOC/sources
		checkReceivers $LOC/IntentResults/sendOtherActions.txt $LOC/IntentResults/permissions.txt $LOC/sources
	fi
	#if [ -s actionNotFound.txt ]
	#then
		checkBroadcasts $LOC/IntentResults/allStrings.txt $LOC/IntentResults/permissions.txt $LOC/sources
		checkActivities $LOC/IntentResults/allStrings.txt $LOC/IntentResults/permissions.txt $LOC/sources
		checkServices $LOC/IntentResults/allStrings.txt $LOC/IntentResults/permissions.txt $LOC/sources
		checkReceivers $LOC/IntentResults/allStrings.txt $LOC/IntentResults/permissions.txt $LOC/sources
	#fi
fi

cat $LOC/IntentResults/permissions.txt >> $LOC/OurPermissions

#############################################################################
# WRITE_EXTERNAL_STORAGE and INTERNET permission special cases
#############################################################################

if [ $REFLECTIONONLY = false ]; then

	if [ -e $LOC/specialperms.txt ]
	then
		rm $LOC/specialperms.txt
	fi
	touch $LOC/specialperms.txt

	if grep -q "sdcard" $LOC/IntentResults/allStrings.txt 
	then
		echo "android.permission.WRITE_EXTERNAL_STORAGE" >> $LOC/specialperms.txt
	fi

	if [ -d $LOC/baksmali/res ]
	then
		SAVEIFS=$IFS
		IFS=$(echo -en "\n\b")
		XML=$(find $LOC/baksmali/res -name "*.xml")
		for x in $XML
		do
			if grep -q "WebView" $x
			then
				echo "android.permission.INTERNET" >> $LOC/specialperms.txt
				echo "$x includes a WebView [android.permission.INTERNET]" >> $LOC/sources
			fi
			if grep -qi "sdcard" $x
			then
				echo "android.permission.WRITE_EXTERNAL_STORAGE" >> $LOC/specialperms.txt
				echo "$x includes a sdcard path [android.permission.WRITE_EXTERNAL_STORAGE]" >> $LOC/sources
			fi
		done
		IFS=$SAVEIFS
	fi
fi

cat $LOC/specialperms.txt >> $LOC/OurPermissions

#############################################################################
# PROVIDER ANALYSIS
#############################################################################

if [ $REFLECTIONONLY = false ]; then
	if [ ! -d $LOC/ProviderResults ] 
	then
		mkdir $LOC/ProviderResults
	fi
	./provideranalysis.rb $LOC/dedex/ $LOC/ProviderResults/
	./providerperms.py $LOC/ProviderResults/URIuse.txt >> $LOC/ProviderResults/providerpermissions.txt 2>> $LOC/sources
fi

cat $LOC/ProviderResults/providerpermissions.txt >> $LOC/OurPermissions

#############################################################################
# PERSISTENT ACTIVITIES
#############################################################################

if grep -q "android:persistent=\"true\"" $LOC/AndroidManifest.xml
then
	echo "android.permission.PERSISTENT_ACTIVITY" >> $LOC/OurPermissions
	echo "AndroidManifest.xml contains a persistent activity [android.permission.PERSISTENT_ACTIVITY]" >> $LOC/sources
fi

#############################################################################
# REPORTING
#############################################################################

sort -u $LOC/OurPermissions > $LOC/tmp
mv $LOC/tmp $LOC/OurPermissions
#cat $LOC/OurPermissions
./getuses.rb $LOC/AndroidManifest.xml > $LOC/orig 

if [ -e $LOC/Underprivilege ]
then
	rm $LOC/Underprivilege
fi
if [ -e $LOC/Overprivilege ]
then
	rm $LOC/Overprivilege
fi

./compare.py $LOC/orig $LOC/OurPermissions $LOC

correct=true
if [ -e $LOC/Underprivilege ]
then
	echo "The application is underprivileged."
	correct=false
fi
if [ -e $LOC/Overprivilege ]
then
	echo "The application is overprivileged."
	amount=$(wc -l $LOC/Overprivilege )
	correct=false
fi
if $correct ; then
	echo "We agree about permissions."
fi
