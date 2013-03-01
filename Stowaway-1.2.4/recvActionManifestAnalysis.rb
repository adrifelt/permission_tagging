#!/usr/bin/ruby
#Prints all unique actions required by the app's components to files (separated by component type: activity, receiver, service)
#Arg1: path and filename of the XML
#Arg2: output folder (with '/')

require "rexml/document"
include REXML

$activity_actions=[]
$broadcast_actions=[]
$service_actions=[]

def getActions(components, array)
	for c in components
		c.elements.to_a("./intent-filter/action").each do |a|
			#puts a.attributes["android:name"]
			array.push(a.attributes["android:name"])
		end
	end
end

def main()
	filename = ARGV[0]
	outputdir = ARGV[1]	

	file = File.new(filename)
	doc = REXML::Document.new file

	all_activities = doc.elements.to_a("//activity")
	all_alias = doc.elements.to_a("//activity-alias")
	all_receivers = doc.elements.to_a("//receiver")
	all_services = doc.elements.to_a("//service")

	#puts "***Activity actions***"
	getActions(all_activities+all_alias, $activity_actions)
	#puts "***Receiver actions***"	
	getActions(all_receivers, $broadcast_actions)
	#puts "***Service actions***"	
	getActions(all_services, $service_actions)

	#puts "***Summary***"
	#puts  $activity_actions.uniq
	#puts  $broadcast_actions.uniq
	#puts  $service_actions.uniq
	
	File.open(outputdir+"recvActivityActions.txt", 'w+') do |f|
		$activity_actions.uniq.each do |name|
			f.write("#{name}\n")
		end
	end 
	File.open(outputdir+"recvBroadcastActions.txt", 'w+') do |f|
		$broadcast_actions.uniq.each do |name|
			f.write("#{name}\n")
		end
	end 
	File.open(outputdir+"recvServiceActions.txt", 'w+') do |f|
		$service_actions.uniq.each do |name|
			f.write("#{name}\n")
		end
	end 

end

main()

