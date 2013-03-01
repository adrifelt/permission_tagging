#!/usr/bin/ruby
require "rexml/document"
include REXML


class Component
attr_accessor :name, :visibility, :type, :permission, :attack, :ifAlias, :strength, :uses, :hasProtectedBC, :hasAnyProtectedBC, :isMain, :isLauncher, :actions, :hasExportedFlag, :hasExportedFlagTrue, :hasData, :categories, :target
def initialize(n, v, t)
	@name=n					#name of component
	@visibility=v			#whether it's public or private
	@type=t					#activity, receiver, provider, service, activity-alias, dynamicreceiver
	@permission=""			#permission it requires, if applicable
	@attack=""				#attack type
	@ifAlias=""				#if activity-alias, the name of the real activity
	@hasExportedFlag = false #whether the developer made it explicitly public or private
	@hasExportedFlagTrue = false #whether the developer made it explicitly public
	@hasData = false

  @target = "" #if determines the br target for dynamic receivers
	
	@uses=[]				#which methods use the info from an intent, set in calling program
	@strength=0				#whether it uses the intent, set in calling program

	@actions=[]				#all actions in declares in its intent filters	
	@hasProtectedBC=false	#whether it has only protected broadcast actions in its intent filters
	@hasAnyProtectedBC=false
	@isLauncher=false		#whether it has the LAUNCHER category
	@isMain=false			#whether it has the MAIN action
	@categories=[]

end
end

def getProtectedBroadcasts()
	f = File.new("Resources/protectedbroadcast.txt")
	protected_Broadcasts = []
	begin
		while (line = f.readline)
			line.chomp!
			protected_Broadcasts.push(line)
		end
	rescue EOFError
		f.close
	end
	
	return protected_Broadcasts
end

def getName(c)
	name=c.attributes["android:name"]
	if name and (name[0]==46)
		name = $packageName+name
	elsif name and not name.include?('.')
		name = $packageName+"."+name
	end
	return name
end

def getAliasName(c)
	name=c.attributes["android:targetActivity"]
	if name and (name[0]==46)
		name = $packageName+name
	elsif name and not name.include?('.')
		name = $packageName+"."+name
	end
	return name
end

def getVisibility(tag)
	attr = tag.attributes["android:exported"] 
	if attr and attr.downcase == "true"
		puts "Found Exported=True"
		return true
	elsif attr and attr.downcase == "false"
		puts "Found Exported=False"
		return false
	end
	filter = tag.elements.to_a("./intent-filter/action")
	if filter.size > 0
		return true
	else
		puts "No intent filter, hidden component" if $options[:debug]
		return false
	end
end

def hasExportedFlag(tag)
  attr = tag.attributes["android:exported"]
  if attr
    return (attr.downcase == "true" or attr.downcase == "false")
  else
    return false
  end
end

def hasExportedFlagTrue(tag)
	attr = tag.attributes["android:exported"] 
	if attr and attr.downcase == "true"
		return true
	else
		return false
	end
end

def hasData(tag)
	datacount = tag.elements.to_a("./intent-filter/data")
	if datacount.length > 0
		return true
	end
	return false
end

def getType(c)
	c.name
end

def getProtectionLevel(p)
	level = p.attributes["android:protectionLevel"]
	case level
	when "normal"
		return 0
	when "dangerous"
		return 1
	when "signature"
		return 2
	when "signatureOrSystem"
		return 3
	when /^\d$/
		if level.to_i >=0 and level.to_i < 4
			return level.to_i
		else
			puts "!!!Invalid protection level"
			return -1
		end
	else
		puts "!!!Invalid protection level"
		return -1
	end
end

def getApplicationPermissions(doc)
	app = doc.elements.to_a("/manifest/application")
	app_perm = app[0].attributes["android:permission"]
	if app.size >1 
		puts "!!!Multiple application permissions in manifest!!!"
	end
	if app_perm != nil
		puts "Application requires #{$app_perm}" if $options[:verbose]
	end
	
	return app_perm
end

def getDefinedPermissions(doc)
	defined_permissions = {}
	permissions = doc.elements.to_a("//permission")
	for p in permissions
		level = getProtectionLevel(p)
		name=p.attributes["android:name"]
		defined_permissions[name]=level
		puts "Defines permission #{name}" if $options[:verbose]
	end
	
	return defined_permissions
end

def getUsesPermissions(doc)
	has_permissions = []
	permissions = doc.elements.to_a("//uses-permission")
	for p in permissions
		name=p.attributes["android:name"]
		has_permissions.push(name)
		puts "Uses permission #{name}" if $options[:verbose]
	end
	
	return has_permissions
end

def getComponents(doc, app_perm, protected_Broadcasts)
	component_names= []
	components = {}
	requires_permissions = {}
	
	all_providers = doc.elements.to_a("//provider")
	all_activities = doc.elements.to_a("//activity")
	all_receivers = doc.elements.to_a("//receiver")
	all_services = doc.elements.to_a("//service")
	all_alias = doc.elements.to_a("//activity-alias")

	all_components = all_providers+all_activities+all_receivers+all_services+all_alias

	for c in all_components:
		name = getName(c)
		component_names.push(name)
		components[name]=Component.new(name, getVisibility(c), getType(c))
		puts "Component: #{name} #{components[name].type}" if $options[:verbose]
		components[name].hasExportedFlag = hasExportedFlag(c)
		components[name].hasExportedFlagTrue =  hasExportedFlagTrue(c)
		components[name].hasData =  hasData(c)
		
		perm=c.attributes["android:permission"]
		if perm != nil
			components[name].permission=perm
			requires_permissions[components[name]] = perm
			puts "Setting component permission: #{components[name].name}, #{perm}" if $options[:verbose] 
		elsif app_perm != nil
			components[name].permission=app_perm
			requires_permissions[components[name]] = app_perm
			puts "Setting component permission #{components[name].name}, #{app_perm}" if $options[:verbose]
		end
		if components[name].type =="activity-alias"
			components[name].ifAlias=getAliasName(c)
		end

		protectedBC=false
		anyprotectedBC=false
		c.elements.to_a("./intent-filter/action").each do |a|
			if protected_Broadcasts.include?(a.attributes["android:name"])
				protectedBC=true
			else
				protectedBC=false
				break
			end
		end
		if protectedBC==true
			components[name].hasProtectedBC=true
		end

		c.elements.to_a("./intent-filter/action").each do |a|
			if protected_Broadcasts.include?(a.attributes["android:name"])
				anyprotectedBC=true
				break
			end
		end
		if anyprotectedBC==true
		  components[name].hasAnyProtectedBC=true
		end
	
		c.elements.to_a("./intent-filter/action").each do |a|
			actionName = a.attributes["android:name"]
			components[name].actions.push(actionName)
			if (actionName == "android.intent.action.MAIN")
				components[name].isMain = true
			end
		end
		c.elements.to_a("./intent-filter/category").each do |a|
			components[name].categories.push(a.attributes["android:name"])
			if (a.attributes["android:name"] == "android.intent.category.LAUNCHER")
				components[name].isLauncher = true
			end
		end
		
		
	end
	
	return component_names, components, requires_permissions
end

def processManifest(filename)
	file = File.new(filename)
	doc = REXML::Document.new file

	$packageName = doc.root.attributes["package"]
	if $packageName.nil?
		puts "***Package Name is nil***"
		exit
	end
	
	protected_Broadcasts = getProtectedBroadcasts()
	
	app_perm = getApplicationPermissions(doc)
	defined_permissions = getDefinedPermissions(doc)
	has_permission = getUsesPermissions(doc)
	component_names, components, requires_permissions = getComponents(doc, app_perm, protected_Broadcasts)

	return protected_Broadcasts, app_perm, defined_permissions, has_permission, component_names, components, requires_permissions, $packageName  
end
