#!/usr/bin/ruby

require 'optparse'
require 'rexml/document'
require 'IntentObj'
require 'FieldObj'
require 'SinkObj'
require 'ParseManifest'
require 'Register'

$options = {}
$vulnerabilityTypes = ['activityhijacking', 'activityhijackingresult', 'servicehijacking',
'servicehijackingresult', 'broadcastexposure', 'broadcastresultmodification', 
'activityhijackingChooser', 'activityhijackingresultChooser', 'ahchooser0', 'ahchooser1', 
'ah0', 'ah1', 'sh0', 'sh1', 'be0', 'be1', 
'intentsniffing', 'intenttheft',
'is0', 'is1', 'it0', 'it1', 
'maliciousactivitylaunch', 'maliciousservicelaunch', 'maliciousbroadcastinjection', 
'mal0', 'mal1', 'msl0', 'msl1', 'mbi0', 'mbi1', 
'proA', 'proR', 'proS', 
'protectedR0', 'protectedR1', 'protectedA0', 'protectedA1', 'protectedS0', 'protectedS1', 
'expToActivity', 'expToService', 'expToReceiver',
'flagRead', 'flagWrite']


class IntentAnalysis
attr_accessor :outfolder, :all_warnings, :vuln_wo_Default_Category, :getStats, :receivingActions, :sendingActions, :setActionNotFound, :all_setActions, :setDestinationNotFound, :all_setDestinations, :allExplicitMsgs, :fixedVulnComponentCount, :fixedVulnIntentCount, :changedComponentCount, :changedIntentCount, :package_name, :getActionCount, :stopServiceCount, :launcherCount, :actionMisuseCount, :sendingWarningCount, :recvingWarningCount
def initialize
  @appname= ""

  @class_name  = ""
  @class_super = ""
  @source_file = ""

  @in_method=false
  @method_name = ""
  @method_code =[]
  @code = {}

  @method_names = []

  @line = nil
  @line_num = ""	#line num with reference to source code
  @line_count = ""  #line num with reference to method

  ## added
  @intents = {}
  @intent_names = []

  @sinks = {}
  @sink_names = []

  @protection_levels={}

  @package_name=""

  @acceptable_distance = 20

  @vulnerabilities= {}
  $vulnerabilityTypes.each do |type|
    @vulnerabilities[type]=0
  end

  @counts ={}
  @counts['activity']=0
  @counts['service']=0
  @counts['receiver']=0

  @counts['asink']=0
  @counts['ssink']=0
  @counts['bsink']=0

  @dynBR_files=[]

  @investigate_methods=[]
  @investigate_methods1=[]
  
  @methods_for_class={}				#array of methods for each class
  @methods_in_class=[]

  @methods_with_getIntent={}			#method, use level
  @methods_with_intent_param={}		#method, use level
  @method_calls_getIntent={}			#method, array of other methods called
  @method_calls_param={}				#method, array of other methods called

  @method_returns_string={}
  @method_returns_intent=[]
  @method_returns_explicit_intent={}
  @method_returns_extra_intent={}
  @method_returns_read_intent={}
  @method_returns_write_intent={}

  @method_returns_action_intent={}

  @weird_errors= []
  @check_perms= []

  @intent_filters={}

  @count_components={}
  @outfolder=""
  @infolder=""
  
  @components = {}			#components
  @component_names = []		#component names
  @has_permissions = []		#uses-permission
  @defined_permissions = {}   #permissions to be added to protection-level list
  @requires_permissions = {}	#permissions that the components require to interact
  @app_perm = ""				#permission that the app requires to interact
  @protected_Broadcasts=[]
  @knownAndroidIntents = []
  @vuln_components = []
  @vuln_intents = []
  
  @all_warnings = []
  @vuln_wo_Default_Category = []
  
  @fields={}
  
  @all_setActions= []
  @setActionNotFound = {}
  
  @all_setDestinations= []
  @setDestinationNotFound = {}

  @receivingActions={}
  @sendingActions={}
  @allExplicitMsgs={}
  
  @callGraph={}
  @reverseCallGraph = {}
  
  @other_action_location=[]
  
  @all_strings=[]
  
  @fixedVulnComponentCount=0
  @fixedVulnIntentCount=0
  @changedComponentCount=0
  @changedIntentCount=0
  @getActionCount=0
  @stopServiceCount=0
  @launcherCount=0
  @actionMisuseCount=0
  @sendingWarningCount=0
  @recvingWarningCount=0 #include protectedBC bug
end


######################################
def get_cmd_args()
		optparse = OptionParser.new do |opts|

				opts.on( '-h', '--help', 'Display this screen' ) do
						puts opts
						exit
				end 

				$options[:verbose] = false
				opts.on("-v", "--[no-]verbose", "Run verbosely") do |v|
						$options[:verbose] = v
				end
				
				$options[:debug] = false
				opts.on("-d","--debug", "Debug info") do
				    $options[:debug] = true
				end

				$options[:intents] = false
				opts.on("-i","--intents", "Intent info") do
				    $options[:intents] = true
				end
				
				$options[:stowaway] = false
				opts.on("-s","--stowaway", "Stowaway Output") do
				    $options[:stowaway] = true
				end
				
				$options[:comdroid] = false
				opts.on("-c","--comdroid", "ComDroid Output") do
				    $options[:comdroid] = true
				end

				$options[:measurements] = false
				opts.on("-m","--measurements", "Measurements") do
				    $options[:measurements] = true
				end

		end
		optparse.parse!
end

def banner(str)
	puts
	#puts "******************************************************************************************"
	puts str
	puts "******************************************************************************************"
end

def get_file_list(fn)
		#puts fn
		f = File.new(fn)
		fl = []
		begin
				while (line = f.readline)
						line.chomp!
						fl.push(line)
				end
		rescue EOFError
				f.close
		end
		fl
end

def reset()
		@method_name = ""
		@method_code = []
		@in_method = false
		@line_count = 0
end

################Utils
def canonicalize_method_name(method)
		path = ""
		if (@class_name.split(' ').size == 1 ) then
			path = @class_name	
		else
			sr = @class_name.split(' ')
			path += sr[sr.size - 1] 
		end

		path += "/"
		if (method.split(' ').size != 1 ) then
			sr = method.split(' ')
			method=sr[sr.size - 1] # add method name
		end
		lastParen = method.index(")") 
		path += method[0..lastParen]			#strip_method_name_args(method)
		path
end

def slash_to_dot(str)
	return str.split('/').join('.')
end

def get_code(method)
	return @code[method]
end

def get_reg_range(range, param_pos)
	range =~ /v([0-9]+)..v([0-9]+)/
	pos=$1.to_i + param_pos
	if pos > $2.to_i
		puts "Range register is not correct!!!***"
	end
	reg="v"+pos.to_s
	return reg
end

def get_register(line, param_pos)
	reg = ""
	if (line =~ /^.*\{(.*)\}.*/) then
		if $1.index("..") !=nil then
			return get_reg_range($1, param_pos)
		else
			params = $1.split(',')
			if params.size() > param_pos then
				reg = params[param_pos]
			else
				puts "***Bad register position"
			end
		end
	else
		puts "***Parse register error"
	end
	return reg
end

def vuln_increment(type)
	@vulnerabilities[type]= @vulnerabilities[type]+1
end

def hasStrongProtection(perm)
	if ! @protection_levels.has_key?(perm)
		puts "!!!Permission level for permission check not found: #{perm}"
		return false
	end
	return @protection_levels[perm] >= 3
end
#################
def record_methods(fn)
	f = File.new(fn)
	begin
		while (@line = f.readline)
			parse_for_method(@line)
		end
	rescue EOFError
		f.close
	end
end

def parse_for_method(line)
	if (/\S/ !~ line) then 
		return
	end
	
	if (@in_method == true) then
		@method_code.push(line.strip)
		@line_count= @line_count+1
		
		if (line.strip =~ /^invoke-\S+\s+\{.*\},(\S+)\s*;.*(\(.*\))/)
      call= $1
      params=$2
      if (!call.start_with?("android/") && !call.start_with?("java/"))
        if @callGraph.has_key?(@method_name)
          @callGraph[@method_name] = @callGraph[@method_name].push("#{call}#{params}")
        else
          @callGraph[@method_name] = ["#{call}#{params}"]
        end
      end
    end
	end

	if (line.strip =~ /^\.(class|super|source|field|method|limit|line|end|inner|implements|annotation|interface) (.*)/) then
		handle_line(line.strip, $1, $2)	
	elsif(line.strip =~ /^const-(string)\s+(v[0-9]+),\"(.*)\"/)
		@all_strings.push($3)
	elsif(line.strip =~ /^invoke-static.*;.*\)Landroid\/content\/Intent;/)
		#static return of intent
		record_intent(line.strip, "-1")
	elsif(line.strip =~ /^invoke-virtual.*\/registerReceiver.*\((.*)\)/)
		name = "#{slash_to_dot(@class_name)}*#{@method_name}@#{@line_count}"
		@component_names.push(name)
		@components[name]=Component.new(name, true, "dynamicreceiver")
		puts "Register receiver: #{name}"
		@investigate_methods.push(@method_name)
	elsif(line.strip =~ /^invoke-direct.*\{(.*)\},android\/content\/IntentFilter\/<init>\s*;\s*<init>\((.*)*\)/)
		record_intentFilter()
		@investigate_methods.push(@method_name)
	elsif(line.strip =~ /^invoke-static\s*\{(.*)\},android\/content\/IntentFilter\/create\s*;\s*create\(Ljava\/lang\/String;Ljava\/lang\/String;\)/)
		record_intentFilter()
		@investigate_methods.push(@method_name)		
	elsif(line.strip =~ /^invoke-.*\/(checkPermission|checkCallingOrSelfPermission|checkCallingOrSelfUriPermission|checkCallingPermission|checkCallingUriPermission|checkUriPermission)\s*;.*\(/)
		puts "!!!Found #{$1}"
		puts "#{line}"
		@check_perms.push("#{@method_name}@#{@line_count}")
		@investigate_methods.push(@method_name)
	elsif(line.strip =~ /^invoke-.*\},android\/content\/Intent\/.*;.*\)Landroid\/content\/Intent;/)
		#do nothing if returned intent is from the same class
	elsif(line.strip =~ /^invoke-.*;.*\)Landroid\/content\/Intent;/)
		#non-static return of intent
		record_intent(line.strip, "-1")
	elsif(line.strip  =~ /^invoke.*\{.*\},android\/content\/Intent\/<init>/) then
		reg = get_register(line.strip, 0)
		record_intent(line.strip, reg)
		if (line.strip  =~ /\(Ljava\/lang\/String;\)/)
		  @setActionNotFound["#{@method_name}@#{@line_count}"]=true
		elsif (line.strip  =~ /\(Ljava\/lang\/String;Landroid\/net\/Uri;\)/)
		  @setActionNotFound["#{@method_name}@#{@line_count}"]=true
		elsif (line.strip  =~ /\(Ljava\/lang\/String;Landroid\/net\/Uri;Landroid\/content\/Context;Ljava\/lang\/Class;\)/)
      @setActionNotFound["#{@method_name}@#{@line_count}"]=true
      @setDestinationNotFound["#{@method_name}@#{@line_count}"]=true
    elsif (line.strip  =~ /\(Landroid\/content\/Context;Ljava\/lang\/Class;\)/)
      @setDestinationNotFound["#{@method_name}@#{@line_count}"]=true
    end
	elsif(line.strip  =~ /^invoke-direct.*\{.*\},android\/content\/BroadcastReceiver\/<init>/) then
		if @class_name.index(/\$\d/) != nil
			puts "Found BroadcastReceiver #{slash_to_dot(@class_name)}"
			@dynBR_files.push(slash_to_dot(@class_name))
		end
	elsif(line.strip =~ /.line (\d+)/)
	  @line_num = $1
	elsif(line.strip =~ /^invoke-virtual.*\/(startService|stopService|bindService|startActivityForResult|startActivityFromChild|startActivity|sendBroadcast|sendOrderedBroadcast|sendStickyBroadcast|sendStickyOrderedBroadcast)\s*;.*\(Landroid\/content\/Intent;.*/)
		record_sink(line.strip, $1)
	end
	
	if (line.strip =~ /^invoke-.*\s+\{.*\},android\/content\/Intent\/setAction\s*;.*/)
	  @setActionNotFound["#{@method_name}@#{@line_count}"]=true
	elsif (line.strip =~ /^invoke-.*\s+\{.*\},android\/content\/Intent\/(setClassName|setClass|setPackage|setComponent).*/)
	  @setDestinationNotFound["#{@method_name}@#{@line_count}"]=true
	end
end

def record_intentFilter()
	@intent_filters["#{@method_name}@#{@line_count}"]=[]
end

def record_sink(line, call_type)
	compType=""
	case call_type
		when /Activity/
			compType="activity"
		when /Service/
			compType="service"
		when /Broadcast/
			compType="broadcast"
		else
			puts "!!!Call type for sink could not be determined"
	end
	a = SinkObj.new(@method_name, @line_count, @line_num, "", call_type, compType)
	name = a.name
	puts "Sink: #{name}" if $options[:verbose] 
	@sink_names.push(name)
	@sinks[name]=a
end

def record_intent(line, register)
	#Handles Intent that is initialized
	if (register) then
		a = IntentObj.new(@method_name, @line_count, line, @line_num)
		a.source_line_num=@line_num
		puts "Intent: #{a.name}" if $options[:verbose]
		a.addregister(register)
		if register != "-1"
			a.is_init=true
		end
		@intent_names.push(a.name)
		@intents[a.name]=a
	#Handles intent that is passed as param
	elsif (line.strip =~ /^\.method/) then
		@methods_with_intent_param[@method_name]=0
		a = IntentObj.new(@method_name, @line_count, @line, @line_num)
		puts "Method: #{a.name}" if $options[:verbose]
		a.isMethodParam=true
		@intent_names.push(a.name)
		@intents[a.name]=a
	#########Need to handle static calls to get intent
	else
		puts "!!!Found intent but did not find input params!!!"
	end
end

def handle_line(line, directive, data)
	case directive
	when "class"
			@class_name = data.split(' ').last
	when "super"
			@class_super = data
	when "source"
			@source_file = data
	when "field"
		  parsed = line.strip.split('=')
		  fieldinfo = parsed[0].strip.split(' ')
		  type=fieldinfo[-1].delete(';')
		  name=fieldinfo[-2]
		  a = FieldObj.new(name, @class_name, type)
		  if parsed.size>1 && parsed[1].include?("\"")
			  value = parsed[1].strip.delete('\"')
			  a.value=value
		  end
		  @fields[a.name] = a
	when "method"
			@line_count = 0
			@in_method = true
			@method_code.push(line.strip)
			@method_name = canonicalize_method_name(data)
			@method_names.push(@method_name)
			@methods_in_class.push(@method_name)
			
			if @method_name.include?("<clinit>()")
				@investigate_methods1.push(@method_name)
			elsif @method_name.include?("<init>")
				@investigate_methods1.push(@method_name)
			end
			if (line.strip =~ /.*Landroid\/content\/Intent;.*/)
				#puts "Intent as a method parameter"
				record_intent(line.strip, nil)
			end
			if (line.strip =~ /.*\)Landroid\/content\/Intent;.*/)
				@method_returns_intent.push(@method_name)
				puts "Found method that returns intent: #{@method_name}"
			end
			if (line.strip =~ /.*\)Ljava\/lang\/String;.*/)
				@method_returns_string[@method_name]=""
				puts "Found method that returns string: #{@method_name}"
			end
	when "limit"
			#nothing
	when "inner"

	when "implements"

	when "annotation"

	when "line"
			@line_num = data
	when "end"
			if data.strip == "method" then
				save_method_code()
			end
	when "interface"
		@class_name = data.split(' ').last
	end
end

def save_method_code()
		#Adding method code for the method code table
		@code[@method_name]=@method_code
		reset()
end

def look_for_values(method, code, first, params)
 	puts "Starting another run #{method}" if $options[:debug]
	vregisters={}
	@line_num=-1
	code.each_with_index.each() do |line, i|
		case line
		when /^;\s+parameter\[(\d+)\]\s+:\s+(v\d+)\s+\(Landroid\/content\/Intent;\)/
		  place = $1.to_i
			if first!=0 && params != [] && params[place] != nil
				recordRegister($2, "intent", params[place], vregisters)
				puts "intent (param): #{params[place]}, #{$2}"  if $options[:debug]
			else
			  recordRegister($2, "intent", "intent:#{method}@0", vregisters)
			  puts "intent (param): #{method}@0, #{$2}"  if $options[:debug]
			end
		when /^;\s+parameter\[(\d+)\]\s+:\s+(v\d+)\s+\(Ljava\/lang\/String;\)/
		  place = $1.to_i
			if first!=0 && params != [] && params[place] != nil
				recordRegister($2, "string", params[place], vregisters)
				puts "string (param): #{params[place]}, #{$2}"  if $options[:debug]
			end
		when /^.line\s+(\d+)/
			@line_num = $1
		when /^const-(string)\s+(v[0-9]+),\"(.*)\"/
			recordRegister($2, $1, $3, vregisters)
			puts "string (const): #{$3}, #{$2}"  if $options[:debug]
		when /^const-(class)\s+(v[0-9]+),(.*)/
			recordRegister($2, $1, $3, vregisters)
			puts "class (const): #{$3}, #{$2}"  if $options[:debug]
		when /^const\/(high16)\s+(v[0-9]+),(.*)/
			recordRegister($2, $1, $3, vregisters)
			puts "high16 (const): #{$3}, #{$2}"  if $options[:debug]
		#when /^const\/4\s+(v[0-9]+),0/
		#  recordRegister($1, "zero", 0, vregisters)
		when /^const-\S+\s+(v[0-9]+),.*/
			removeRegister($1, vregisters)			
		when /^invoke-.*\s+\{.*\},java\/lang\/String\/valueOf\s*;\s*valueOf\(Ljava\/lang\/Object;\)Ljava\/lang\/String;/
		  reg = get_register(line, 0)
		  if correctRegisterType(reg, "string", vregisters)
	      return_reg = find_return_register(code, i)
			  if return_reg != "-1"
				  recordRegister(return_reg, "string", vregisters[reg].value, vregisters)
				  puts "string (valueOf): #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
			  end
			end
		when /^invoke-.*\s+\{.*\},java\/lang\/StringBuilder\/<init>.*(\(.*\)).*/
			params = $1
			case params
			when "()", "(Z)"
				reg = get_register(line, 0)
				recordRegister(reg, "stringbuilder", "", vregisters)
				puts "stringbuilder: \"\", #{reg}" if $options[:debug]
			when "(Ljava/lang/String;)"
				reg = get_register(line, 0)
				reg1 = get_register(line, 1)
				if correctRegisterType(reg1, "string", vregisters)
					recordRegister(reg, "stringbuilder",  vregisters[reg1].value, vregisters)
					puts "stringbuilder: #{vregisters[reg1].value}, #{reg}" if $options[:debug]
				end
			end
		when /^invoke-.*\s+\{.*\},java\/lang\/StringBuilder\/append.*(\(.*\)).*/
			params = $1
			case params
			when "(Ljava/lang/String;)"
				reg = get_register(line, 0)
				reg1 = get_register(line, 1)
				if correctRegisterType(reg1, "string", vregisters) && correctRegisterType(reg, "stringbuilder", vregisters)
					return_reg = find_return_register(code, i)
					if return_reg != "-1"
						recordRegister(return_reg, "stringbuilder",  "#{vregisters[reg].value}#{vregisters[reg1].value}", vregisters)
						puts "stringbuilder: (append) #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
						if return_reg != reg
							recordRegister(reg, "stringbuilder",  vregisters[return_reg].value, vregisters)
							puts "stringbuilder: (append) #{vregisters[reg].value}, #{reg}" if $options[:debug]
						end
					else
						recordRegister(reg, "stringbuilder",  "#{vregisters[reg].value}#{vregisters[reg1].value}", vregisters)
            puts "stringbuilder: (append) #{vregisters[reg].value}, #{reg}" if $options[:debug]
					end
				end
			else
				reg = get_register(line, 0)
				if correctRegisterType(reg, "stringbuilder", vregisters)
					return_reg = find_return_register(code, i)
					if return_reg != "-1"
						recordRegister(return_reg, "stringbuilder",  "#{vregisters[reg].value}?", vregisters)
						puts "stringbuilder: (append) #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
						if return_reg != reg
							recordRegister(reg, "stringbuilder",  vregisters[return_reg].value, vregisters)
							puts "stringbuilder: (append) #{vregisters[reg].value}, #{reg}" if $options[:debug]
						end
					else
						recordRegister(reg, "stringbuilder",  "#{vregisters[reg].value}?", vregisters)
						puts "stringbuilder: (append) #{vregisters[reg].value}, #{reg}" if $options[:debug]
					end
				end
			end
		when /^invoke-.*\s+\{.*\},java\/lang\/StringBuilder\/toString\s*;/
			reg = get_register(line, 0)
			if correctRegisterType(reg, "stringbuilder", vregisters)
				return_reg = find_return_register(code, i)
				recordRegister(return_reg, "string",  vregisters[reg].value, vregisters)
				puts "string: (toString) #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
			end

 		when /^sput-object\s+(v[0-9]+),(.*) (.*)/
 			reg = $1
 			param = $2
 			type = $3
 			if vregisters.has_key?(reg)
 				if @fields.has_key?(param)
 					@fields[param].value = vregisters[reg].value
 					puts "Saving #{vregisters[reg].value} to #{param}" if $options[:debug]
 				else
 					puts "!!!!!COULD NOT FIND FIELD KEY: #{param}"
 				end
 			end
 		when /^sget-object\s+(v[0-9]+),(.*) (.*)/
 			reg = $1
 			param = $2
 			type = $3 		
 			if @fields.has_key?(param)
 				value = @fields[param].value
 				if type == "Landroid/content/Intent;"
 				  recordRegister(reg, "intent", value, vregisters)
 				  puts "Loading #{vregisters[reg].value} to #{param}" if $options[:debug]
 				elsif type == "Ljava/lang/String;"
 					recordRegister(reg, "string", value, vregisters)
 				  puts "Loading #{vregisters[reg].value} to #{param}" if $options[:debug]
 				end
 			end
		when /^iput-object\s+(v[0-9]+),(v[0-9]+),(.*) (Ljava\/lang\/String|Landroid\/content\/IntentFilter|Landroid\/content\/Intent)/
			reg = $1
			ignore = $2			#we are treating this as a static var,
			param = $3
			if vregisters.has_key?(reg)			  
				if @fields.has_key?(param)
					@fields[param].value = vregisters[reg].value
					puts "Saving #{vregisters[reg].value} to #{param}"  if $options[:debug]
				else
					puts "!!!!!COULD NOT FIND FIELD KEY: #{param}"
				end
			else
			  #$stderr.puts("Did not have value to store")
			end

		when /^iget-object\s+(v[0-9]+),(v[0-9]+),(.*) (Ljava\/lang\/String|Landroid\/content\/IntentFilter|Landroid\/content\/Intent)/
			reg = $1
			ignore = $2
			param = $3
			type = $4
			if @fields.has_key?(param)
				value = @fields[param].value
				puts "Loading #{value} from #{param} to #{reg}" if $options[:debug]
				#must not have semicolon in end
				case type
				when "Ljava/lang/String"
					recordRegister(reg, "string", value, vregisters)
				when "Landroid/content/IntentFilter"
  				recordRegister(reg, "intentfilter", value, vregisters)
				when "Landroid/content/Intent"
					recordRegister(reg, "intent", value, vregisters)
				end
			end
		when /^invoke-virtual.*\{.*\},java\/lang\/Object\/getClass\s*;/
			reg = get_register(line, 0)
			secondline = code[i+1]
			classvalue = get_comment_type(secondline, reg)
			if classvalue != false
			  return_reg = find_return_register(code, i)
			  if classvalue == "Ljava/lang/Object"
				  if correctRegisterType(reg, "object", vregisters)
					  classvalue = vregisters[reg].value
				  end
			  end
			  if classvalue.start_with?("L")
			    classvalue = classvalue[1..-1]
			  end
			  recordRegister(return_reg, "class", slash_to_dot(classvalue), vregisters)
			  puts "class: (getClass) #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
		  end
		when /invoke-.*	\{(.*)\},java\/lang\/Class\/(getSimpleName|getName)\s*;/
		  funcName = $2
			reg = get_register(line, 0)
			if correctRegisterType(reg, "class", vregisters)
				return_reg = find_return_register(code, i)
				if funcName == "getSimpleName"
				  recordRegister(return_reg, "string", slash_to_dot(vregisters[reg].value).split(".")[-1], vregisters)
				else
				  recordRegister(return_reg, "string", slash_to_dot(vregisters[reg].value), vregisters)
				end
				puts "string: (get(Simple)Name) #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
			end
		when /invoke-.*\{(.*)\},java\/lang\/Class\/forName\s*;/
			reg1 = get_register(line, 0)
			if correctRegisterType(reg1, "string", vregisters)
				return_reg = find_return_register(code, i)
				if return_reg != "-1"
					recordRegister(return_reg, "class", slash_to_dot(vregisters[reg1].value), vregisters)
				end
			end
			
		when /^invoke-virtual.*\{.*\},dalvik\/system\/DexClassLoader\/loadClass\s*;/
  		reg = get_register(line, 1)
  		return_reg = find_return_register(code, i)
  		if correctRegisterType(reg, "string", vregisters)
  			recordRegister(return_reg, "class", vregisters[reg].value, vregisters)
  			puts "class: #{vregisters[reg].value}, #{return_reg}"
  		end
			
		when /^invoke-virtual.*\{.*\},java\/lang\/ClassLoader\/loadClass\s*;/
  		reg = get_register(line, 1)
  		return_reg = find_return_register(code, i)
  		if correctRegisterType(reg, "string", vregisters)
  			recordRegister(return_reg, "class", vregisters[reg].value, vregisters)
  			puts "class: #{vregisters[reg].value}, #{return_reg}"
  		end
		
			
		when /^new-instance\s+(v[0-9]+),android\/content\/Intent$/
			recordRegister($1, "intent", "intent", vregisters)
			puts "Add Instance Reg: #{vregisters[$1].name} #{vregisters[$1].getType} #{vregisters[$1].value}" if $options[:debug]
		when /^new-instance\s+(v[0-9]+),/
			removeRegister($1, vregisters)
		when /^move-object.*(v[0-9]+),(v[0-9]+)/
			reg1=$1
			reg2=$2
			if vregisters.has_key?(reg2)
				recordRegister(reg1, vregisters[reg2].getType, vregisters[reg2].value, vregisters)
				vregisters[reg1].copyLinks(vregisters[reg2])
				vregisters[reg2].addLink(reg1)
				vregisters[reg1].addLink(reg2)
				puts "Update Reg (move): #{vregisters[reg1].name} #{vregisters[reg1].getType} #{vregisters[reg1].value}" if $options[:debug]
			elsif vregisters.has_key?(reg1) && (! vregisters.has_key?(reg2))
				puts "Deleting Reg (move): #{vregisters[reg1].name}"  if $options[:debug]
				vregisters.delete(reg1)
			end
		when /^invoke-direct.*android\/content\/ComponentName\/<init>.*\(.*;.*;\)/
			reg1 = get_register(line, 0)
			reg2 = get_register(line, 2)
			if correctRegisterType(reg2, "string", vregisters) || correctRegisterType(reg2, "class", vregisters)
				recordRegister(reg1, "componentname", vregisters[reg2].value, vregisters)
        puts "componentName: #{vregisters[reg2].value}, #{reg1}" if $options[:debug]
			else
				recordRegister(reg1, "componentname", "", vregisters)
				puts "componentName: \"\", #{reg1}" if $options[:debug]
			end
		when /^invoke-direct.*android\/content\/ComponentName\/<init>.*\(.*;\)/
			puts "!!!Could not parse this ComponentName!!!"
		when /^invoke-direct.*\{.*\},android\/content\/Intent\/<init>.*(\(.*\)).*/
			params = $1
			reg = get_register(line, 0)
			name = method+"@"+i.to_s
			if ! hasRegister(reg, vregisters)
				recordRegister(reg, "intent", "intent:#{name}", vregisters)
				puts "intent (init): #{vregisters[reg].value}, #{reg}" if $options[:debug]
			else
				vregisters[reg].setRegister(reg, "intent", "intent:#{name}")
				vregisters[reg].linkedTo.each do |r|
					puts "Copying other intents" if $options[:debug]
					if ! hasRegister(r, vregisters)
						recordRegister(r, "intent", "intent:#{name}", vregisters)
						puts "intent (init): #{vregisters[r].value}, #{r}" if $options[:debug]
					end
					vregisters[r].setRegister(r, "intent", "intent:#{name}")
				end
			end

			puts "Found init, src_line:#{@line_num}, ddx_line:#{i}" if $options[:verbose]
			if @intent_names.include?(name)
				intent = @intents[name]
				intent.line=line
				case params
				when "()"
					intent.type=1
				when "(Ljava/lang/String;)"
					intent.type=2
					reg = get_register(line, 1)
					if correctRegisterType(reg, "string", vregisters)
						intent.action.push(vregisters[reg].value)
						@all_setActions.push(vregisters[reg].value)
						@setActionNotFound["#{method}@#{i}"]=false
						puts "  added action: #{vregisters[reg].value}" if $options[:debug]
					else
						puts "!!!Intent constructor: could not find action"
						add_weird_error("!!!Intent constructor: could not find action")
					end
				when "(Landroid/content/Intent;)"
					intent.type=3
					reg = get_register(line, 1)
					if correctRegisterType(reg, "intent", vregisters)
						if vregisters[reg].value=~/intent:(.*)/
							intent2=@intents[$1]
							if intent2.explicit
								intent.explicit = true
								intent.explicit_destination=intent2.explicit_destination
							end
							intent.action.concat(intent2.action)
						else
							puts "!!!Intent copy constructor: could not find src intent"
						end
					else
						puts "!!!Intent copy constructor: could not find src intent"
					end
				when "(Landroid/content/Context;Ljava/lang/Class;)"
					intent.type=4
					reg = get_register(line, 2)
					setExplicitDestination(intent, reg, "class", vregisters, "#{method}@#{i}")
					puts "  added explicit dest" if $options[:debug]
				when "(Ljava/lang/String;Landroid/net/Uri;)"
					intent.type=5
					intent.hasURI=true
					action_reg = get_register(line, 1)
					action_type = get_comment_type(code[i+1], action_reg)
					if correctRegisterType(action_reg, "string", vregisters)
						intent.action.push(vregisters[action_reg].value)
						@all_setActions.push(vregisters[action_reg].value)
						@setActionNotFound["#{method}@#{i}"]=false
						puts "  added action: #{vregisters[action_reg].value}" if $options[:debug]
				  elsif action_type == "single-length"
				    @setActionNotFound["#{method}@#{i}"]=false
				    puts "  action is null: #{action_reg}" if $options[:debug]
					else
						puts "!!!Intent constructor: could not find action"
						add_weird_error("!!!Intent constructor: could not find action")
					end
				when "(Ljava/lang/String;Landroid/net/Uri;Landroid/content/Context;Ljava/lang/Class;)"
					intent.type=6
					reg = get_register(line, 4)
					setExplicitDestination(intent, reg, "class", vregisters, "#{method}@#{i}")
					intent.hasURI=true
					action_reg = get_register(line, 1)
					action_type = get_comment_type(code[i+1], action_reg)
					if correctRegisterType(action_reg, "string", vregisters)
						intent.action.push(vregisters[action_reg].value)
						@all_setActions.push(vregisters[action_reg].value)
						@setActionNotFound["#{method}@#{i}"]=false
						puts "  added action: #{vregisters[action_reg].value}" if $options[:debug]
					elsif action_type == "single-length"
				    @setActionNotFound["#{method}@#{i}"]=false
				    puts "  action is null: #{action_reg}" if $options[:debug]
					else
						puts "!!!Intent constructor: could not find action"
						add_weird_error("!!!Intent constructor: could not find action")
					end

				else
					puts "!!!Intent type not handled!!!"
				end
			else
				puts line
				puts "Could not find intent!!!"
			end
		when /^invoke-.*\s+\{.*\},android\/content\/Intent\/parseUri.*/
		  return_reg = find_return_register(code, i)
		  if return_reg != "-1"
		    recordRegister(return_reg, "intent", "intent:#{method}@#{i}", vregisters)
		    puts "intent (parseUri), has VIEWaction: #{return_reg}" if $options[:debug]
		    @intents["#{method}@#{i}"].action.push("android.intent.action.VIEW")
		    @intents["#{method}@#{i}"].hasURI=true
		  end
		when /^invoke-.*\s+\{.*\},android\/content\/Intent\/putExtra.*/
			reg = get_register(line, 0)
			if correctRegisterType(reg, "intent", vregisters)
				if vregisters[reg].value=~/intent:(.*)/
					intent=@intents[$1]
					intent.hasExtra=true
					return_reg = find_return_register(code, i)
          if return_reg != "-1"
            recordRegister(return_reg, vregisters[reg].getType, vregisters[reg].value, vregisters)
            puts "intent (putExtra): return to #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
          end
				end
			else
				puts "!!!Could not find intent register"##: putExtra"
			end
		when /^invoke-.*\s+\{.*\},android\/content\/Intent\/setAction.*/
			reg = get_register(line, 0)
			action_reg = get_register(line,1)
			if correctRegisterType(action_reg, "string", vregisters)
				@all_setActions.push(slash_to_dot(vregisters[action_reg].value))
				@setActionNotFound["#{method}@#{i}"]=false
			end
			if correctRegisterType(reg, "intent", vregisters)
				if vregisters[reg].value=~/intent:(.*)/
					intent=@intents[$1]
					action_reg = get_register(line,1)
					if correctRegisterType(action_reg, "string", vregisters)
						intent.action.push(slash_to_dot(vregisters[action_reg].value))
						puts "intent (setAction): #{vregisters[action_reg].value}, #{action_reg}" if $options[:debug]
					else
						puts "Set action: could not find action"
					end
					return_reg = find_return_register(code, i)
          if return_reg != "-1"
            recordRegister(return_reg, vregisters[reg].getType, vregisters[reg].value, vregisters)
            puts "  intent (setAction): move to #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
          end
				end
			else
				puts "!!!Could not find intent register"##: setAction, #{line}"
			end
		when /^invoke-.*\s+\{(.*)\},android\/content\/Intent\/createChooser/
			reg = get_register(line, 0)
			if correctRegisterType(reg, "intent", vregisters)
				if vregisters[reg].value=~/intent:(.*)/
					intent=@intents[$1]
					intent.hasChooser=true
					puts "intent (createChooser): has chooser, #{reg}" if $options[:debug]
				end
				code[i+1..i+4].each do |x|
					if x=~ /^move-result-object\s+(v\d+)/
						reg1=$1
						if hasRegister(reg, vregisters)
							recordRegister(reg1, vregisters[reg].getType, vregisters[reg].value, vregisters)
							puts "  intent (createChooser): move to #{vregisters[reg1].value}, #{reg1}" if $options[:debug]
							vregisters[reg1].copyLinks(vregisters[reg])
							vregisters[reg].addLink(reg1)
							vregisters[reg1].addLink(reg)
							break
						end
					end
				end
			else
				puts "!!!Could not find intent register"##: createChooser"
			end
			
		when /^invoke-.*\s+\{(.*)\},android\/content\/Intent\/(set|add)Flag/
			reg = get_register(line, 0)
			reg1 = get_register(line, 1)
			if correctRegisterType(reg, "intent", vregisters) && correctRegisterType(reg1, "high16", vregisters)
				if vregisters[reg].value=~/intent:(.*)/
					intent=@intents[$1]
					if (vregisters[reg1].value.to_i & 2 == 2)
						intent.hasFlagWrite = true
					end
					if (vregisters[reg1].value.to_i & 1 == 1)
						intent.hasFlagRead = true
					end
					return_reg = find_return_register(code, i)
          if return_reg != "-1"
            recordRegister(return_reg, vregisters[reg].getType, vregisters[reg].value, vregisters)
            puts "  intent (set|add)Flag: move to #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
          end
				else
					##
				end
			else
				puts "!!!Could not find intent register"##: (set|add)Flag"
			end	
		when /^invoke-.*\s+\{(v[0-9]+),.*\},android\/content\/Intent\/(setClassName|setClass).*/
			reg = $1
			methodtype = $2
			reg2 = get_register(line, 2)
			if correctRegisterType(reg, "intent", vregisters)
				if vregisters[reg].value=~/intent:(.*)/
					intent=@intents[$1]
					if methodtype == "setClass"
						setExplicitDestination(intent, reg2, "class", vregisters, "#{method}@#{i}")
					else
						setExplicitDestination(intent, reg2, "string", vregisters, "#{method}@#{i}")
					end
					puts "intent (setClass(Name)): #{intent.name}, #{reg}" if $options[:debug]
					return_reg = find_return_register(code, i)
          if return_reg != "-1"
            recordRegister(return_reg, vregisters[reg].getType, vregisters[reg].value, vregisters)
            puts "  intent (setClass(Name)): move to #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
          end
				end
			else
				puts "!!!Could not find intent register"##: (setClassName|setClass)"
			end
		when /^invoke-.*\s+\{(v[0-9]+),.*\},android\/content\/Intent\/setComponent.*/
			reg = $1
			reg2 = get_register(line, 1)
			if correctRegisterType(reg, "intent", vregisters)
				if vregisters[reg].value=~/intent:(.*)/
					intent=@intents[$1]
					setExplicitDestination(intent, reg2, "componentname", vregisters, "#{method}@#{i}")
					puts "intent (setComponent): #{intent.name}, #{reg}" if $options[:debug]
					return_reg = find_return_register(code, i)
          if return_reg != "-1"
            recordRegister(return_reg, vregisters[reg].getType, vregisters[reg].value, vregisters)
            puts "  intent (setComponent): move to #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
          end
				end
			else
				puts "!!!Could not find intent register"##: setComponent"
			end
		
		when /^invoke-.*\s+\{(v[0-9]+),.*\},android\/content\/Intent\/setPackage.*/
			reg = $1
			reg2 = get_register(line, 1)
			if correctRegisterType(reg, "intent", vregisters)
				if vregisters[reg].value=~/intent:(.*)/
					intent=@intents[$1]
					setExplicitDestination(intent, reg2, "string", vregisters, "#{method}@#{i}")
					puts "intent (setPackage): #{intent.name}, #{reg}" if $options[:debug]
					return_reg = find_return_register(code, i)
          if return_reg != "-1"
            recordRegister(return_reg, vregisters[reg].getType, vregisters[reg].value, vregisters)
            puts "  intent (setPackage): move to #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
          end
				end
			else
				puts "!!!Could not find intent register"##: setPackage"
			end
		when /^invoke-direct.*\{(.*)\},android\/content\/IntentFilter\/<init>\s*;\s*<init>\(\)/
			reg=get_register(line, 0)
			recordRegister(reg, "intentfilter", "#{method}@#{i.to_s}", vregisters)
			puts "intentfilter (init): #{vregisters[reg].value}, #{reg}" if $options[:debug]
		when /^invoke-direct.*\{(.*)\},android\/content\/IntentFilter\/<init>\s*;\s*<init>\((Ljava\/lang\/String;)+\)/
			reg=get_register(line, 0)
			recordRegister(reg, "intentfilter", "#{method}@#{i.to_s}", vregisters)
			puts "intentfilter (init): #{vregisters[reg].value}, #{reg}" if $options[:debug]
			reg1=get_register(line, 1)
			if correctRegisterType(reg1, "string", vregisters)
				@intent_filters["#{method}@#{i.to_s}"].push(slash_to_dot(vregisters[reg1].value))
				puts "  intentfilter action: #{vregisters[reg1].value}, #{reg}" if $options[:debug]
			end
		when /^invoke-static.*\{(.*)\},android\/content\/IntentFilter\/create\s*;\s*create\(Ljava\/lang\/String;Ljava\/lang\/String;\)/
			code[i+1..i+4].each do |x|
				if x=~ /^move-result-object\s+(v\d+)/
					reg1=$1
					recordRegister(reg1, "intentfilter", "#{method}@#{i.to_s}", vregisters)
					puts "intentfilter (create): #{vregisters[reg1].value}, #{reg1}" if $options[:debug]
					break
				end
			end
			reg=get_register(line, 0)
			if correctRegisterType(reg, "string", vregisters)
				@intent_filters["#{method}@#{i.to_s}"].push(slash_to_dot(vregisters[reg].value))
				puts "  intentfilter action: #{vregisters[reg].value}, #{reg1}" if $options[:debug]
			end
		when /^invoke-.*\s+\{(.*)\},android\/content\/IntentFilter\/addAction\s*;\s*addAction\(Ljava\/lang\/String;\)/
			reg=get_register(line, 0)
			if correctRegisterType(reg, "intentfilter", vregisters)
				reg1=get_register(line, 1)
				if correctRegisterType(reg1, "string", vregisters)
					@intent_filters[vregisters[reg].value].push(slash_to_dot(vregisters[reg1].value))
					puts "  intentfilter (addAction): #{vregisters[reg1].value}, #{reg}" if $options[:debug]
				end
			end
    when /^invoke-virtual.*\{(.*)\},(.*)\/getPackageName\s*;\s*getPackageName\(\)Ljava\/lang\/String;/
      return_reg = find_return_register(code, i)
			if return_reg != "-1"
      	recordRegister(return_reg, "string", @package_name, vregisters)
				puts "string (getPackageName): #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
			end
		when /^invoke-virtual.*\{(.*)\},.*\/(sendBroadcast|sendOrderedBroadcast|sendStickyBroadcast|sendStickyOrderedBroadcast)\s*;.*\(Landroid\/content\/Intent;.*/
			reg5=get_register(line, 1)
			methodType=$2
			if correctRegisterType(reg5, "intent", vregisters)
				if vregisters[reg5].value=~/intent:(.*)/
					intent=@intents[$1]
					intent.dest_type="broadcast"
					sink_found(method, intent, line, i, @line_num)
					name ="#{method}@#{i.to_s}"
					puts "Found Broadcast Sink, src_line:#{@line_num}, ddx_line:#{i}" if $options[:verbose]
					case line
					when /sendBroadcast\(Landroid\/content\/Intent;Ljava\/lang\/String;.*\)/
						reg = get_register(line, 2)
						if correctRegisterType(reg, "string", vregisters)
							@sinks[method+"@"+i.to_s].permission = vregisters[reg].value
						else
							puts "Incorrect permission register"
						end
					when /sendOrderedBroadcast\(Landroid\/content\/Intent;Ljava\/lang\/String;.*\)/
						reg = get_register(line, 2)
						if correctRegisterType(reg, "string", vregisters)
							@sinks[method+"@"+i.to_s].permission = vregisters[reg].value
						else
							puts "Incorrect permission register"
						end
					end
				else
					puts "Could not find intent, line:#{@line_num}, instead of intent its #{vregisters[reg5].value}"
				end
			else
				puts "!!!Broadcast's intent param not found: #{method}, #{@line_num}"
			end
		when /^invoke-virtual.*\{(.*)\},.*\/(startActivityForResult|startActivityFromChild|startActivity)\s*;.*\(Landroid\/content\/Intent;.*/
			reg5=get_register(line, 1)
			if correctRegisterType(reg5, "intent", vregisters)
				if vregisters[reg5].value=~/intent:(.*)/
					intent=@intents[$1]
					intent.dest_type="activity"
					sink_found(method, intent, line, i, @line_num)
					puts "Found Activity Sink, src_line:#{@line_num}, ddx_line:#{i}" if $options[:verbose]
				else
					puts "Could not find intent for sink, line:#{@line_num}, instead of intent its #{vregisters[reg5].value}"
				end
			else
				puts "!!!Activity's intent param not found: #{method}, #{@line_num}"
			end
		when /^invoke-virtual.*\{(.*)\},.*\/(startService|stopService|bindService)\s*;.*\(Landroid\/content\/Intent;.*/
			reg5=get_register(line, 1)
			if correctRegisterType(reg5, "intent", vregisters)
				if vregisters[reg5].value=~/intent:(.*)/
					intent=@intents[$1]
					intent.dest_type="service"
					sink_found(method, intent, line, i, @line_num)
					puts "Found Service Sink, src_line:#{@line_num}, ddx_line:#{i}" if $options[:verbose]
				else
					puts "Could not find intent, line:#{@line_num}, instead of intent its #{vregisters[reg5].value}"
				end
			else
				puts "!!!Service's intent param not found: #{method}, #{@line_num}"
			end
		when /^invoke-static\s+\{(.*)\},android\/app\/PendingIntent\/(getBroadcast|getActivity|getService).*/
			reg5=get_register(line, 2)
			type = $2
			if (correctRegisterType(reg5, "intent", vregisters))
				#Should I follow to subsequent calls?
				if vregisters[reg5].value=~/intent:(.*)/
					intent=@intents[$1]
					case type
					when "getBroadcast" 
						intent.dest_type="Pbroadcast"
					when "getActivity" 
						intent.dest_type="Pactivity"
					when "getService" 
						intent.dest_type="Pservice"
					else 
						puts "!!!Other Type of Pending Intent!!!"
					end
					sink_found(method, intent, line, i, @line_num, false)
					puts "Found Pending Intent Sink, src_line:#{@line_num}, ddx_line:#{i}" if $options[:verbose]
				else
					puts "Could not find intent, line:#{@line_num}"
				end
			else	
				puts "Found PendingIntent but incorrect"
			end
		when /^invoke-virtual.*\/registerReceiver.*\((.*)\)/
			params=$1.split(';')
			classType=method.split('(')[0].split('/')[0..-2].join('.')
			name="#{classType}*#{method}@#{i}"
			reg =  get_register(line, 2)
			if correctRegisterType(reg, "intentfilter", vregisters)
			  if @intent_filters.has_key?(vregisters[reg].value)
			    @components[name].actions=@intent_filters[vregisters[reg].value]
				  actions=@intent_filters[vregisters[reg].value]
				  puts " registerReceiver: #{vregisters[reg].value}, #{reg}" if $options[:debug]
				  protectedBC=false
				  actions.each do |a|
					  if @protected_Broadcasts.include?(a)
						  protectedBC=true
					  else
						  protectedBC=false
						  break
					  end
				  end
				  if protectedBC==true
					  @components[name].hasProtectedBC=true
				  end

				  anyprotectedBC=false
				  actions.each do |a|
					  if @protected_Broadcasts.include?(a)
						  anyprotectedBC=true
						  break
					  end
				  end
				  if anyprotectedBC==true
					  @components[name].hasAnyProtectedBC=true
				  end

				else
				  #$stderr.puts("Found registerReceiver but intentfilter not initialized: #{method} ")
				end
			else
				regs = code[i+1].split(',')
				regs.each do |r|
					if r=~/#{reg}\s+:\s+(.*)\s+/
						if $1 != "Landroid/content/IntentFilter;"
							puts "registerReciever intent filter type: #{$1}"
							@components[name].visibility=false
						end
						break
					end
				end
			end
			if params.size == 4
				reg =  get_register(line, 3)
				if correctRegisterType(reg, "string", vregisters)
					puts "registerReceiver with permission #{vregisters[reg].value}"
					@components[name].permission = vregisters[reg].value
				else
					#do nothing, it's null
				end
			end
			reg =  get_register(line, 1)
			secondline = code[i+1]
			brType = get_comment_type(secondline, reg)
			if brType != false
			  br = slash_to_dot(brType[1..-1])
			  if (br != "android.content.BroadcastReceiver" && @methods_for_class.has_key?(br))
			    @components[name].target = br
			  end
			end
		when /^invoke-virtual\s+\{(v\d+)\},android\/content\/Intent\/clone\s*;/
			reg2=$1
			#puts "Found cloned intent"
			found=false
			if correctRegisterType(reg2, "intent", vregisters)
				code[i+1..i+4].each do |x|
					if x=~ /^move-result-object\s+(v\d+)/
						reg1=$1
						name = method+"@"+i.to_s
						recordRegister(reg1, vregisters[reg2].getType, vregisters[reg2].value, vregisters)
    			  puts " intent clone: #{vregisters[reg1].value}, #{reg1}" if $options[:debug]
						vregisters[reg1].copyLinks(vregisters[reg2])
						vregisters[reg2].addLink(reg1)
						vregisters[reg1].addLink(reg2)
						found=true
						break
					end
				end
				if not found
					puts "but could not find return value"
				end
			end

		when /^invoke-.*\},android\/content\/Intent\/.*;.*\)Landroid\/content\/Intent;/
			#Intent returned from intent class
			reg2 =  get_register(line, 0)
			code[i+1..i+4].each do |x|
				if x=~ /^move-result-object\s+(v\d+)/
					#puts "Content/Intent that returns intent is saved"
					reg1=$1
					if hasRegister(reg2, vregisters)
						recordRegister(reg1, vregisters[reg2].getType, vregisters[reg2].value, vregisters)
						puts "returns Intent to: #{vregisters[reg1].value}, #{reg1}" if $options[:debug]
						vregisters[reg1].copyLinks(vregisters[reg2])
						vregisters[reg2].addLink(reg1)
						vregisters[reg1].addLink(reg2)
					end
					break
				end
			end
			
			

		when /^invoke-.*\{(.*)\},(\S*)\s*;.*(\(.*\))(.*)/
			regs=$1
			hasParam=$3
			meth="#{$2}#{$3}"
			returntype=$4.split(";")[0]
			params = get_param_regs(regs)
      if (@method_names.include?(meth) && first<1 && (hasParam.include?("Ljava/lang/String") || hasParam.include?("Landroid/content/Intent")))
     		if not line =~ /^invoke-static/
     		  params = params[1..-1]
     		end
     		array = make_param_array(params, vregisters)
     		puts "call with (string|intent) param" if $options[:debug]
     		returnvalue = look_for_values(meth, @code[meth], first+1, array)
     		if returnvalue
     		  return_reg = find_return_register(code, i)
     		  if returntype =="Ljava/lang/String"
            recordRegister(return_reg, "string", returnvalue, vregisters)
            puts "Recording returned string #{returnvalue}, #{return_reg}" if $options[:debug]
          elsif returntype =="Landroid/content/Intent"
            recordRegister(return_reg, "intent", returnvalue, vregisters)
            puts "Recording returned intent #{returnvalue}, #{return_reg}" if $options[:debug]
            if returnvalue =~/intent:(.*)/
              puts " #{$1} Explicit?: #{@intents[$1].explicit} Action: #{@intents[$1].action}" if $options[:debug]
            end
          end
        end
      elsif @method_names.include?(meth)
        puts "Found call - no recursion" if $options[:debug]
        if hasParam.include?("Landroid/content/Intent")
          puts "2x Found a method call that sends an intent: #{line}" if $options[:debug]
  				if code[i+1]=~/.*(v\d+)\s+:\s+Landroid\/content\/Intent;.*/
  					reg = $1
  					if correctRegisterType(reg, "intent", vregisters)
  						if vregisters[reg].value=~/intent:(.*)/
  							intent=@intents[$1]
  							if intent.explicit
  								@intents["#{meth}@0"].explicit=true
  								@intents["#{meth}@0"].explicit_destination = intent.explicit_destination
  								puts "Found method call that sends an intent with explicit destination"
  							end
  							@intents["#{meth}@0"].action.concat(intent.action)
  						end
  					else
  						puts "!!!Method call that sends intent did not have correct type"
  					end
  				end
        end
        
        case returntype
        when "Landroid\/content\/Intent"
          return_reg = find_return_register(code, i)
          name = method+"@"+i.to_s
  				recordRegister(return_reg, "intent", "intent:#{name}", vregisters)
  				puts " returns Intent to: #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
          if @method_names.include?("#{meth}")
  					if @method_returns_explicit_intent.has_key?("#{meth}")
  							intent=@intents[name]
  							intent.explicit=true
  							puts "  Returned intent was explicit" if $options[:debug]
  					end
  					if @method_returns_extra_intent.has_key?("#{meth}")
  							intent=@intents[name]
  							intent.hasExtra=true
  							puts "  Returned intent had extras" if $options[:debug]
  					end
  					if @method_returns_read_intent.has_key?("#{meth}")
  							intent=@intents[name]
  							intent.hasFlagRead=true
  							puts "  Returned intent has Read" if $options[:debug]
  					end
  					if @method_returns_write_intent.has_key?("#{meth}")
  							intent=@intents[name]
  							intent.hasFlagWrite=true
  							puts "Returned intent has Write" if $options[:debug]
  					end
  					if @method_returns_action_intent.has_key?("#{meth}")
  							intent=@intents[name]
  							intent.action.concat(@method_returns_explicit_intent["#{meth}"])
  							puts "  Returned intent had action" if $options[:debug]
  					end
  				end   
        when "Ljava\/lang\/String"
          return_reg = find_return_register(code, i)
          if return_reg != "-1"
    			  if @method_returns_string.has_key?("#{meth}") && @method_returns_string["#{meth}"] != ""
          	  recordRegister(return_reg, "string", @method_returns_string["#{meth}"], vregisters)
    				  puts " Returned string: #{vregisters[return_reg].value}, #{return_reg}" if $options[:debug]
    			  end
    			end
        end
      elsif line=~/^invoke.*\s+\S+\s*;\s*getIntent\(\)Landroid\/content\/Intent;/
        #Handle getIntent
  			return_reg = find_return_register(code, i)
  			recordRegister(return_reg, "intent", "intent:#{method}@#{i}", vregisters)
        puts "getIntent: #{return_reg}" if $options[:debug]

  			@methods_with_getIntent[method]=0
  		elsif line=~/^invoke.*\s+\S+\s*;\s*.*\(.*\)Landroid\/content\/Intent;/
        #Handle getIntent
  			return_reg = find_return_register(code, i)
  			recordRegister(return_reg, "intent", "intent:#{method}@#{i}", vregisters)
        puts "something that returns an Intent: #{return_reg}, #{line}" if $options[:debug]      
      end
					
		when /return-object\s+(v\d+)/
			reg =$1
			if @method_returns_intent.include?(method) && correctRegisterType(reg, "intent", vregisters)
				if vregisters[reg].value=~/intent:(.*)/
					intent=@intents[$1]
					intent.returned=true
					puts "Found returned intent: #{intent.name}"
					if intent.explicit == true
						@method_returns_explicit_intent[intent.method]=intent.explicit_destination
					end
					if intent.hasExtra == true
						@method_returns_extra_intent[intent.method]=true
					end
					if intent.hasFlagRead == true
						@method_returns_read_intent[intent.method]=true
					end
					if intent.hasFlagWrite == true
						@method_returns_write_intent[intent.method]=true
					end
					if intent.action != []
						@method_returns_write_intent[intent.method]=intent.action
					end
				end
			elsif @method_returns_string.include?(method) && correctRegisterType(reg, "string", vregisters)
  			@method_returns_string[method] = vregisters[reg].value
			end
			
			if first!=0
			  if hasRegister(reg, vregisters)
					puts "Returning #{vregisters[reg].value} #{method}"
					return vregisters[reg].value
				else
					return nil
				end
			end
			
		end
	end
end

def make_param_array(params, vregisters)
	array = []
	params.each do |p|
		if hasRegister(p, vregisters)
			array.push(vregisters[p].value)
		else
			array.push(nil)
		end
	end
	return array
end

def get_param_regs(paramregstring)
	if paramregstring.index("..") !=nil then
	  if paramregstring =~ /v([0-9]+)..v([0-9]+)/
	    start = $1.to_i
      last = $2.to_i
	    array = []
	    start.upto(last) { |i| array.push("v#{i}")}
	    return array
	  else
  		puts "***Parse register error"
	  end
	else
	  return paramregstring.split(",")
	end
end

def get_comment_type(line, reg)
  if line.include?(",")
	  regs = line.split(',')
	  regs.each do |r|
		  if r=~/#{reg}\s+:\s+(.*);/
			  return $1
			elsif r=~/#{reg}\s+:\s+(.*)\s*/
  		  return $1.strip
		  end
	  end
	elsif line=~/#{reg}\s+:\s+(.*);/
		return $1
	elsif line=~/#{reg}\s+:\s+(.*)\s*/
		return $1.strip
	else
	  return false
	end
end

def find_return_register(code, i)
	code[i+1..i+4].each do |x|
		if x=~ /^move-result-object\s+(v\d+)/
			return $1
		end
	end
	return "-1"
end

def mark_sink(method, pos, intent)
	name=method+"@"+pos.to_s
	if @sink_names.include?(method+"@"+pos.to_s)
		@sinks[name].done = true
		@sinks[name].addIntent(intent)
	else
		puts "***COULD NOT FIND SINK****"
		puts name
	end		
end

def sink_found(method, intent, line, i, src_lnum, marksink=true)
	intent.done=true
	intent.sink_line = line
	#if (src_lnum.to_i - intent.source_line_num.to_i)>@acceptable_distance 
	#	puts "Lines away: #{src_lnum.to_i - intent.source_line_num.to_i}"
	#end
	if marksink
		mark_sink(method, i, intent)
	end
end

def setExplicitDestination(intent, reg, type, vregisters, location)
	intent.explicit=true
	if correctRegisterType(reg, type, vregisters)
		intent.explicit_destination = vregisters[reg].value.split("/").join(".")
		@all_setDestinations.push(vregisters[reg].value.split("/").join("."))
		@setDestinationNotFound[location]=false
	else
		"!!!Incorrect register type"
	end
end

def hasRegister(name, vregisters)
	if vregisters.has_key?(name)
		return true
	else
		return false
	end
end

def correctRegisterType(name, type, vregisters)
	if hasRegister(name, vregisters) && vregisters[name].getType == type
		return true
	else
		return false
	end
end

def removeRegister(reg, vregisters)
	if hasRegister(reg, vregisters)
		vregisters.delete($1)
		vregisters.keys.each do |i|
			if i != reg
				vregisters[i].removeLink(reg)
			end
		end
	end
end

def recordRegister(name, type, value, vregisters)
	reg= Register.new(name, type, value)
	vregisters[name]=reg
end

def checkIntentVulns(sink)
	vulnFound = false
	sink.intents.each do |intent|
		if ! intent.explicit
			vulnFound = true
		end
	end
	return vulnFound
end

def allHasChooser(sink)
	hasChooser = true
	sink.intents.each do |intent|
		if ! intent.hasChooser
			hasChooser = false
		end
	end
	return hasChooser
end

def anyHasExtra(sink)
	hasExtra = false
	sink.intents.each do |intent|
		if intent.hasExtra
			hasExtra = true
		end
	end
	return hasExtra
end

def anyHasRead(sink)
	hasRead = false
	sink.intents.each do |intent|
		if intent.hasFlagRead
			hasRead = true
		end
	end
	return hasRead
end

def anyHasWrite(sink)
	hasWrite = false
	sink.intents.each do |intent|
		if intent.hasFlagWrite
			hasWrite = true
		end
	end
	return hasWrite
end

def write_explicit_file(explicit, done)
	exp=[explicit, done]
	File.open("#{@outfolder}explicitcount", 'w+') do |f|  
		Marshal.dump(exp, f)  
	end 
end

def write_componenttotal_file(total)
	File.open("#{@outfolder}totalcomponents", 'w+') do |f|  
		Marshal.dump(total, f)  
	end 
end


def print_stats()
	puts "Intents: #{@intent_names.size}"
	explicit_count=0
	nonpending_exp_count=0
	nonpending_count=0
	method_count=0
	done_count=0
	sink_count=0
	normal_count=0
	pending_count=0
	other_count=0
	@intent_names.each do |name|
		intent = @intents[name]
		puts intent.name if $options[:verbose]
		if intent.done == true
			done_count=done_count+1
			if intent.dest_type == "broadcast" || intent.dest_type == "activity" || intent.dest_type == "service" 
				nonpending_count=nonpending_count+1
			end
			if intent.explicit ==true
				explicit_count=explicit_count+1
				if intent.dest_type == "broadcast" || intent.dest_type == "activity" || intent.dest_type == "service" 
					nonpending_exp_count=nonpending_exp_count+1
				end
			end
		end
		
		if intent.isMethodParam == true then
			method_count=method_count+1
		elsif intent.is_init == true
			normal_count=normal_count+1
		else
			other_count=other_count+1
		end

		if intent.dest_type == "Pbroadcast" || intent.dest_type == "Pactivity" || intent.dest_type == "Pservice"
			pending_count = pending_count + 1
		end
	end
	puts "Method: #{method_count}"
	puts "Other: #{other_count}"
	puts "Typical: #{normal_count}"
	puts 
	puts "Found sink: #{done_count} of #{@intent_names.size}"
	puts "Explicit: #{explicit_count} of #{done_count}"
	puts "Non-pending Explicit Intents: #{nonpending_exp_count} of #{nonpending_count}"
	puts
	puts "Pending Sinks: #{pending_count}"

	write_explicit_file(explicit_count,done_count)

	@sink_names.each do |name|
		sink = @sinks[name]
		if sink.done==true
			sink_count=sink_count+1
		else
			puts sink.name
		end
	end
	puts "Other Sinks: #{sink_count} of #{@sink_names.size}"
	
	puts

	a_count=0
	s_count=0
	b_count=0
	plainb_count=0
	stickyb_count=0
	orderedb_count=0
	stickyorderedb_count=0
	
	@sink_names.each do |name|
		sink=@sinks[name]
		case sink.compType
		when "activity"
			a_count = a_count+1
		when "service"
			s_count = s_count+1
		when "broadcast"
			b_count = b_count+1
			case sink.type
			when "sendBroadcast"
				plainb_count = plainb_count+1
			when "sendOrderedBroadcast"
				orderedb_count = orderedb_count+1
			when "sendStickyBroadcast"
				stickyb_count = stickyb_count+1
			when "sendStickyOrderedBroadcast"
				stickyorderedb_count = stickyorderedb_count+1
			end
		end
	end

	puts "Activity Sinks: #{a_count}"
	puts "Service Sinks: #{s_count}"
	puts "Broadcast Sinks: #{b_count}"
	puts "	sendBroadcast Sinks: #{plainb_count}"
	puts "	sendOrderedBroadcast Sinks: #{orderedb_count}"
	puts "	sendStickyBroadcast Sinks: #{stickyb_count}"
	puts "	sendStickyOrderedBroadcast Sinks: #{stickyorderedb_count}"

	@counts['asink']=a_count
	@counts['ssink']=s_count
	@counts['bsink']=b_count
	
	File.open("#{@outfolder}sinkcount", 'w+') do |f|  
		Marshal.dump(@counts, f)  
	end 

end

def print_intents()
	@intent_names.each do |name|
		if @intents[name].isMethodParam == false then
			puts "**************************"
			puts @intents[name].name
			puts @intents[name].line
			#puts @intents[name].source_line_num
			puts "Explicit: #{@intents[name].explicit}"
			if @intents[name].explicit == true
				puts "Explicit Destination: #{@intents[name].explicit_destination}"
			end
			#puts "Actions: #{@intents[name].action}"
			puts "Destination Type: #{@intents[name].dest_type}"
			puts "Done: #{@intents[name].done}"
		end
	end
end

def print_components()
	activity_count=0
	service_count=0
	receiver_count=0
	dynamicreceiver_count=0
	alias_count=0
	provider_count=0
	public_count=0
	
	@component_names.each do |name|
		component = @components[name]
		case component.type
		when "activity"
			activity_count=activity_count+1
		when "service"
			service_count=service_count+1
		when "receiver"
			receiver_count=receiver_count+1
		when "dynamicreceiver"
			dynamicreceiver_count=dynamicreceiver_count+1
		when "activity-alias"
			alias_count=alias_count+1
		when "activity-alias"
			alias_count=alias_count+1
		when "provider"
			provider_count=provider_count+1
		end
		if component.visibility == true
			public_count= public_count+1
		end
	end
	puts "Activities: #{activity_count}"
	puts "Services: #{service_count}"
	puts "Receivers: #{receiver_count}"
	puts "DynamicReceivers: #{dynamicreceiver_count}"
	puts "Activity-aliases: #{alias_count}"
	puts "Providers: #{provider_count}"
	puts "Total: #{@component_names.size}"
	puts "Public: #{public_count}"
	if 	activity_count+service_count+receiver_count+alias_count+provider_count+dynamicreceiver_count != @component_names.size
		puts "!!!!!!!!!!Components not accounted for"
	end
	
	@counts['activity']=activity_count+alias_count
	@counts['service']=service_count
	@counts['receiver']=receiver_count+dynamicreceiver_count
end

def print_vulns()
	puts "Exposure to Components"
	puts "Malicious Activity Start: #{@vulnerabilities['maliciousactivitylaunch']} of #{@counts['activity']}"
	puts "Malicious Service Start: #{@vulnerabilities['maliciousservicelaunch']} of #{@counts['service']}"
	puts "Malicious Data Injection: #{@vulnerabilities['maliciousbroadcastinjection']} of #{@counts['receiver']}"
	puts "Protected Activity Vuln: #{@vulnerabilities['proA']}"
	puts "Protected Service Vuln: #{@vulnerabilities['proS']}"
	puts "Protected Receiver Vuln: #{@vulnerabilities['proR']}"

	puts 
	puts "Exposure to Intents"
	puts "Activity Hijacking: #{@vulnerabilities['activityhijacking']} of #{@counts['asink']}"
	puts "Service Hijacking: #{@vulnerabilities['servicehijacking']} of #{@counts['ssink']}"
	puts "Broadcast Exposure: #{@vulnerabilities['broadcastexposure']} of #{@counts['bsink']}"
	puts "	Intent Sniffing: #{@vulnerabilities['intentsniffing']}"
	puts "	Intent Theft: #{@vulnerabilities['intentsniffing']}"
	puts "	Result Modification: #{@vulnerabilities['broadcastresultmodification']}"
	
	puts
	puts "Explicit Intents to Public Components"
	puts "  To Activity: #{@vulnerabilities['expToActivity']}"
	puts "  To Service: #{@vulnerabilities['expToService']}"
	puts "  To Receiver: #{@vulnerabilities['expToReceiver']}"
end

def investigate_methods(to_investigate, method_calls, methods_with_intent_use)
	intent_used=[]
	intent_strengths=[]
	done_investigating=[]
	while to_investigate.size != 0
		if methods_with_intent_use.has_key?(to_investigate.first) && methods_with_intent_use[to_investigate.first] != 0
			intent_used.push(to_investigate.first)
			intent_strengths.push(methods_with_intent_use[to_investigate.first])
		end
		done_investigating.push(to_investigate.first)
		if method_calls.has_key?(to_investigate.first) && method_calls[to_investigate.first] !=[]
			method_calls[to_investigate.first].each do |m|
				if ! done_investigating.include?(m)
					to_investigate.push(m)
				end
			end
		end
		to_investigate.delete(to_investigate.first)
	end
	return intent_used, intent_strengths
end

def find_max(list)
	max=0
	list.each do |i|
		if i>max
			max=i
		end
	end
	return max
end

def component_analysis(component)
	methods=@methods_for_class[component.name]
	intent_used=[]
	intent_strengths=[]
	to_investigate=[]
	done_investigating=[]
	if methods!=nil
		methods.each do |m|
			if not m=~/\/onActivityResult\(/
				if @methods_with_getIntent.has_key?(m)
					if @methods_with_getIntent[m] != 0
						if @method_calls_getIntent[m] !=[]
							to_investigate.concat(@method_calls_getIntent[m])
						end
						intent_used.push(m)
						intent_strengths.push(@methods_with_getIntent[m])
					end
				end
				if @methods_with_intent_param.has_key?(m)
					to_investigate.push(m)
				end
			end
		end
	else
		puts "!!!@methods_for_class[#{component.name}] is nil"
	end

	intent_used2, intent_strengths2=investigate_methods(to_investigate, @method_calls_param, @methods_with_intent_param)
	intent_used.concat(intent_used2)
	intent_strengths.concat(intent_strengths2)
	strength = find_max(intent_strengths)

	return intent_used, strength
end

def elevate_intent_use_level(current, changeTo)
	if changeTo>current
		return changeTo
	else
		return current
	end
end

def look_for_intent_use(method, getIntent)
	vregisters={}
	methods_invoked=[]
	found_intent_use=0
	code = @code[method]
	code.each_with_index.each() do |line, i|
		case line
		when /^;\s+parameter\[\d+\]\s+:\s+(v\d+)\s+\(Landroid\/content\/Intent;\)/
			if getIntent == false
				recordRegister($1, "intent", "intent", vregisters)
			end
		when /^invoke-virtual\s+\S+\s+;\s+getIntent\(\)Landroid\/content\/Intent;/
			if getIntent == true
				found=false
				code[i+1..i+4].each do |x|
					if x=~ /^move-result-object\s+(v\d+)/
						reg=$1
						recordRegister(reg, "intent", "intent", vregisters)
						found=true
						break
					end
				end
				if found == false
					#do nothing, intent is not used
				end
			end

		when /^invoke-(virtual|direct).*,android\/content\/Intent\/get(\S+)\s*;\s+get.*;/
			callType=$2
			reg = get_register(line, 0)
			if hasRegister(reg, vregisters)
				if callType=~/Extra/
					found_intent_use=elevate_intent_use_level(found_intent_use, 1)
				elsif callType=~/getDataString/
					found_intent_use=elevate_intent_use_level(found_intent_use, 1)					
				elsif callType=~/getData/
					found_intent_use=elevate_intent_use_level(found_intent_use, 1)
				else
					found_intent_use=elevate_intent_use_level(found_intent_use, 0)
				end
			else
				puts "Found intent get call but not on an expected intent"
			end
		when /^invoke-virtual\s+\{(v\d+)\},android\/content\/Intent\/clone\s*;/
			reg2=$1
			puts "Found cloned intent"
			found=false
			if correctRegisterType(reg2, "intent", vregisters)
				code[i+1..i+4].each do |x|
					if x=~ /^move-result-object\s+(v\d+)/
						reg1=$1
						name = method+"@"+i.to_s
						recordRegister(reg1, vregisters[reg2].getType, vregisters[reg2].value, vregisters)
						vregisters[reg1].copyLinks(vregisters[reg2])
						vregisters[reg2].addLink(reg1)
						vregisters[reg1].addLink(reg2)
						found=true
						break
					end
				end
				if ! found
					puts "but could not find return value"
				end
			end
		when /^invoke-(.*)\s+\{(.*)\},(\S+)\s*;.*(\(.*Landroid\/content\/Intent;.*\)).*/		
			callType=$1
			meth="#{$3}#{$4}"
			if @method_names.include?(meth)
				getreg=code[i+1]
				if callType!="static"
					getreg=code[i+1].split(',')[1..-1].join(',')
				end
				if getreg=~/.*(v\d+)\s+:\s+Landroid\/content\/Intent;.*/
					if hasRegister($1, vregisters)
						puts "#{meth}"
						methods_invoked.push(meth)
					end
				end
			else
				#ignore
			end
		when /^move-object.*(v[0-9]+),(v[0-9]+)/
			reg1=$1
			reg2=$2
			if vregisters.has_key?(reg2)
				recordRegister(reg1, vregisters[reg2].getType, vregisters[reg2].value, vregisters)
				vregisters[reg1].copyLinks(vregisters[reg2])
				vregisters[reg2].addLink(reg1)
				vregisters[reg1].addLink(reg2)
				puts "Update Reg: #{vregisters[reg1].name} #{vregisters[reg1].getType} #{vregisters[reg1].value}" if $options[:debug]
			elsif vregisters.has_key?(reg1) && ! vregisters.has_key?(reg2) 
				puts "Deleting Reg: #{vregisters[reg1].name}"  if $options[:debug]
				vregisters.delete(reg1)
			end
		end
	end
	
	if getIntent == false
		@methods_with_intent_param[method]=found_intent_use
		@method_calls_param[method]=methods_invoked
	else
		@methods_with_getIntent[method]=found_intent_use
		@method_calls_getIntent[method]=methods_invoked
	end
end

def add_weird_error(str)
	@weird_errors.push(str)
	puts str
end

#DELETE THIS
def checkIntentSending(componentName, componentActions)
	sentToComp = false
	@sink_names.each do |sname|
		sink=@sinks[sname]
		if sink.compType == "broadcast"
			sink.intents.each do |intent|
				if intent.explicit == true && intent.explicit_destination == componentName
					sentToComp = true
				elsif intent.explicit == false && componentActions.size != 0
					hasActions = true
					intent.actions.each do |action|
						if ! componentActions.include?(action)
							hasActions = false
						end
					end
					if intent.actions.size ==0
						hasActions = false
					end
					if hasActions
						sentToComp = true
					end
				end
			end
		end
	end
	return sentToComp
end

def findReverseCallGraph()
  @callGraph.keys.each do |key|
    calls = @callGraph[key]
    calls.each do |call|
      if @method_names.include?(call)
        if @reverseCallGraph.has_key?(call)
          @reverseCallGraph[call] = @reverseCallGraph[call].push(key)
        else
          @reverseCallGraph[call] = [key]
          #puts "Found method"
        end
      else
        #puts "Debugging: not adding #{call}"  
      end
    end
  end
  
  @reverseCallGraph.keys.each do |key|
    @reverseCallGraph[key] = @reverseCallGraph[key].uniq
  end
end

def doesMethodTakeStringParam(meth)
  if meth =~/.*\((.*)\)/
    params = $1
    if params =~/Ljava\/lang\/String/
      return true
    else
      return false
    end
  end
  return false
end

#for any sink where reflection is not successfully found and it takes string,method,cons,or object parameter
def getExtraCallingMethods()
  callingMethods = []
  
  @setActionNotFound.keys.each do |key|
    if key =~/(.*)\@(.*)/
      call=$1
      if (doesMethodTakeStringParam(call) && @reverseCallGraph.has_key?(call))
        @reverseCallGraph[call].delete_if {|x| x == call }
		    callingMethods = callingMethods + @reverseCallGraph[call]
		  end
		end
	end
  
  callingMethods = callingMethods.uniq
  return callingMethods
end


def main()
	puts "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
	get_cmd_args
	@appname = ARGV[0]
	puts @appname
	
	@infolder = "#{ARGV[1]}/"
	@manifestfile = ARGV[2]
	@outfolder = "#{ARGV[3]}/"
	ddxfilelist = "#{@infolder}DDXFILELIST"
	output= "#{@outfolder}vulnstats"
	
	
  if $options[:comdroid]
  	File.open('Resources/permmap') do |f|  
  		@protection_levels=Marshal.load(f)  
  	end

    @knownAndroidIntents = get_file_list("Resources/IntentList.txt")

	  banner("Examining #{@appname} manifest...")
	  @protected_Broadcasts, @app_perm, @defined_permissions, @has_permission, @component_names, @components, @requires_permissions, @package_name = processManifest(@manifestfile)

	  if @defined_permissions != nil
		  @defined_permissions.keys.each do |d|
			  if @protection_levels.has_key?(d) then
				  puts "!!!Permission already exists"
			  else
				  @protection_levels[d] = @defined_permissions[d]
				  puts "Adding protection level for #{d}" if $options[:verbose]
			  end
		  end
	  end
	end

	banner("Examining #{@appname} DDX ...")
	get_file_list(ddxfilelist).each() do |filename|
		record_methods(filename)
		@methods_for_class[slash_to_dot(@class_name)]=@methods_in_class
		@methods_in_class=[]
		@class_name  = ""
		@class_super = ""
		@source_file = ""
	end

	  
  findReverseCallGraph()

	banner("Details...")
	methodstocheck=@investigate_methods1
	methodstocheck=methodstocheck.concat(@method_returns_string.keys)
	methodstocheck=methodstocheck.concat(@method_returns_intent)
	methodstocheck=methodstocheck.concat(@investigate_methods)
	methodstocheck=methodstocheck.uniq
	
  temp = []
	@intents.keys.each do |i|
		temp.push(@intents[i].method)
	end
	@sinks.keys.each do |i|
		temp.push(@sinks[i].inMethod)
	end
	temp=temp.uniq
	
	methodstocheck=methodstocheck.concat(temp)
	methodstocheck.each do |method|
		#puts method if $options[:verbose]
		code = @code[method]
		banner("Processing #{method}...")
		look_for_values(method, code, 0, [])
		puts "***End processing #{method}" #if $options[:verbose]
	end

	banner("Second pass processing...")
  callingMethods = getExtraCallingMethods()
  (callingMethods-methodstocheck).each do |method|
		#puts method if $options[:verbose]
		code = @code[method]
		banner("Processing #{method}...")
		look_for_values(method, code, 0, [])
		puts "***End processing #{method}" #if $options[:verbose]
	end

	banner("Finding methods using intents")
	@methods_with_intent_param.keys.each do |method|
		look_for_intent_use(method, false)
	end
	
	@methods_with_getIntent.keys.each do |method|
		look_for_intent_use(method, true)
	end
	
	#Find classname for dynamic broadcast receivers
	#############################################
	banner("Dynamic receiver resolving...")
	@component_names.each do |name|
		component = @components[name]
		if component.type == "dynamicreceiver" && component.name.include?('*')
		  if component.target!=""
		    ind=@component_names.index(component.name)
        if ind != nil
          puts "Matched register receiver to br" 
          newName = "#{component.target}*#{component.name.split('*')[1]}"
          @component_names[ind]="#{newName}!"
          component.name = "#{newName}!"
          @components["#{newName}!"]=component
          @components.delete(name)
        end

	    else
			  found = false
			  compName=component.name.split('*')[0]
			  location=component.name.split('*')[1]
			  if @dynBR_files !=[]
				  @dynBR_files.each do |brname|
					  if compName == brname.split('$')[0]
						  ind=@component_names.index(component.name)
						  if ind != nil
							  found =true
							  puts "Matched register receiver to br" 
							  @component_names[ind]="#{brname}*#{location}!"
							  component.name = "#{brname}*#{location}!"
							  @components["#{brname}*#{location}!"]=component
							  @components.delete(name)
							  break
						  end
					  end
				  end
			  end
			  if found != true
				  add_weird_error("Could not find br for #{component.name}")
			  end
		  end
		end
	end
	
	classeswithdynbrs=[]
	@dynBR_files.each do |br|
		parentclass=br.split('$')[0]
		if classeswithdynbrs.include?(parentclass)
			add_weird_error("!!!There is more than one dynamic receiver in #{parentclass}")
		else
			classeswithdynbrs.push(parentclass)
		end
	end
	
	#Eliminate
	reduceRedundancies()

end

def logStats()
	banner("Print intent summary") if $options[:intents]
	print_intents() if $options[:intents]
	banner("Print component summary")
	print_components()
	banner("Print intent and sink summary")
	print_stats()

  banner("Print exposure summary")
	print_vulns()

  banner("Found check perms")
	if @check_perms.size == 0
  	puts "Nothing"
	end
  @check_perms.each do |line|
		puts line
  end

  banner("Weird errors")
  if @weird_errors.size == 0
  	puts "Nothing"
  end
  @weird_errors.each do |line|
  	puts line
  end
end
	
def find_component_vulnerabilities()
##################################################
	banner("Find component vulnerabilities")	
	@component_names.each do |name|
		component = @components[name]
		if component.type != "provider"
			if component.type != "dynamicreceiver" && ! @methods_for_class.has_key?(component.name)
				add_weird_error("!!!Component implementation for #{component.name} cannot be found")
				next
			end
			case component.type
			when "activity"
				uses, strength=component_analysis(component)
				component.strength=strength
				component.uses=uses
				if component.isMain == true || component.isLauncher == true
					next
				elsif component.visibility == true && (component.permission == "" || hasStrongProtection(component.permission) == false)
					trackVulnComponents(component.name)
					if component.hasProtectedBC == true
						component.attack="proA"
						puts "Protected Activity: #{component.name}, #{component.strength.to_s}"
						if uses !=[]
							puts "	#{uses}"
						end
						vuln_increment("proA")
						vuln_increment("protectedA#{component.strength.to_s}")
					else
						component.attack="maliciousactivitylaunch"
						text = "Possible Malicious Activity Launch: #{component.name}, #{component.strength.to_s}"
						puts text
						@all_warnings.push(text)
						if uses !=[]
							puts "	#{uses}"
						end
						vuln_increment("maliciousactivitylaunch")
						vuln_increment("mal#{component.strength.to_s}")
						if ! component.categories.include?("android.intent.category.DEFAULT") && ! component.categories.include?("android.intent.category.GADGET")
							@vuln_wo_Default_Category.push("#{component.name}")
						end
					end
				end
			when "service"
				uses, strength=component_analysis(component)
				component.strength=strength
				component.uses=uses
				if  component.visibility == true && (component.permission == "" || hasStrongProtection(component.permission) == false)
					if component.hasProtectedBC == true
						component.attack="proS"
						puts "Protected Service: #{component.name}, #{component.strength.to_s}"
						if uses !=[]
							puts "	#{uses}"
						end
						vuln_increment("proS")
						vuln_increment("protectedS#{component.strength.to_s}")
					else
						trackVulnComponents(component.name)
						component.attack="maliciousservicelaunch"
						text = "Possible Malicious Service Launch: #{component.name}, #{component.strength.to_s}"
						puts text
						@all_warnings.push(text)
						if uses !=[]
							puts "	#{uses}"
						end
						vuln_increment("maliciousservicelaunch")
						vuln_increment("msl#{component.strength.to_s}")
					end
				end
			when "receiver"
				uses, strength=component_analysis(component)
				component.strength=strength
				component.uses=uses
				if  component.visibility == true && (component.permission == "" || hasStrongProtection(component.permission) == false)
					if component.hasProtectedBC == true
						component.attack="proR"
						puts "Protected Receiver: #{component.name}, #{component.strength.to_s}"
						if uses !=[]
							puts "	#{uses}"
						end
						vuln_increment("proR")
						vuln_increment("protectedR#{component.strength.to_s}")
					else
						trackVulnComponents(component.name)
						component.attack="maliciousbroadcastinjection"
						text = "Possible Malicious Broadcast Injection: #{component.name}, #{component.strength.to_s}"
						puts text
						@all_warnings.push(text)
						if uses !=[]
							puts "	#{uses}"
						end
						vuln_increment("maliciousbroadcastinjection")
						vuln_increment("mbi#{component.strength.to_s}")
					end
				end
			end
		else
			#puts "Provider"
		end
	end
	
	brs={}
	@component_names.each do |name|
		component = @components[name]
		if component.type == "dynamicreceiver" && !brs.has_key?(component.name.split('*')[0])
    	br = component.name.split('*')[0]
		  comp=Component.new(br, true, "dynamicreceiver")
		  uses, strength=component_analysis(component)
  		brs[br]=[uses, strength]
  	end
  end

	@component_names.each do |name|
		component = @components[name]
		if component.type == "dynamicreceiver"
			if component.visibility == true && (component.permission == "" || hasStrongProtection(component.permission) == false)
				tempName=name.split('*')[0]
				if brs.has_key?(tempName)
					strength = "undecided"
					uses, strength = brs[tempName]
					component.strength=strength
					component.uses=uses
					
					if component.hasProtectedBC == true
						component.attack="proR"
						puts "Protected Receiver: #{component.name}, #{component.strength.to_s}"
						if uses !=[]
							puts "	#{uses}"
						end
						vuln_increment("proR")
						vuln_increment("protectedR#{component.strength.to_s}")
					else
						trackVulnComponents(component.name)
						if component.name[-1,1] =="!"
						  text = "Possible Malicious Broadcast Injection: #{component.name[0..-2]}, #{component.strength.to_s}"
					  else
				    	text = "Possible Malicious Broadcast Injection: #{component.name}, #{component.strength.to_s}"
  						puts text
  					end
						puts text
						@all_warnings.push(text)
						if uses !=[]
							puts "	#{uses}"
						end
						vuln_increment("maliciousbroadcastinjection")
						if component.strength != "undecided"
							vuln_increment("mbi#{component.strength.to_s}")
						else
							puts "!!!Component strength is undecided, could not find Dyn Broadcast Receiver: #{component.strength.to_s}"
						end
					end
				else
					puts "!!!Could not find broadcast receiver for this registerReceiver call"
				end
			end
		end
	end

	@component_names.each do |name|
		component = @components[name]
		if component.type == "activity-alias"
			if component.isMain == true || component.isLauncher == true
				next
			elsif component.visibility == true && (component.permission == "" || hasStrongProtection(component.permission) == false)
				#No additional analysis needed, just same as it's activity
				component.strength=@components[component.ifAlias].strength
				component.uses=@components[component.ifAlias].uses
				if component.hasProtectedBC == true
					component.attack="proA"
					puts "Protected Activity: #{component.name}, #{component.strength.to_s}"
					if uses !=[]
						puts "	#{uses}"
					end
					vuln_increment("proA")
					vuln_increment("protectedA#{component.strength.to_s}")
				else
					trackVulnComponents(component.name)
					component.attack="maliciousactivitylaunch"
					text = "Possible Malicious Activity Launch: #{component.name}, #{component.strength.to_s}"
					puts text
					@all_warnings.push(text)
					vuln_increment("maliciousactivitylaunch")
					vuln_increment("mal#{component.strength.to_s}")
					if ! component.categories.include?("android.intent.category.DEFAULT") && ! component.categories.include?("android.intent.category.GADGET")
						@vuln_wo_Default_Category.push("#{component.name}")
					end
				end
			end
		end
	end
	
	@count_components['receiver']=0
	@count_components['activity']=0
	@count_components['service']=0
	@component_names.each do |name|
		component = @components[name]
		case component.type 
		when "dynamicreceiver"
			@count_components['receiver']+=1
		when "receiver"
			@count_components['receiver']+=1
		when "activity"
			@count_components['activity']+=1
		when "activity-alias"
			@count_components['activity']+=1
		when "service"
			@count_components['service']+=1
		end
	end
	write_componenttotal_file(@count_components)

end	

def find_intent_vulnerabilities()
##################################################
	banner("Find intent vulnerabilities")
	@sink_names.each do |sname|
		sink=@sinks[sname]
		case sink.compType
		when "activity"
			if checkIntentVulns(sink)
				level=anyHasExtra(sink)
				levelvalue=0
				if level==true
					levelvalue=1
				end
				
				if allHasChooser(sink)
					puts "Possible Activity Hijacking w Chooser: #{sink.name}, Source Line: #{sink.source_line_num}, hasExtras=#{level}"
					vuln_increment("activityhijackingChooser")
					vuln_increment("ahchooser#{levelvalue}")
				else

					hasRead=false
					hasWrite=false
					if anyHasRead(sink)
						vuln_increment("flagRead")
						hasRead=true
					end
					if anyHasWrite(sink)
						vuln_increment("flagWrite")
						hasWrite=true
					end

					trackVulnIntents(sink.name)
					text = "Possible Activity Hijacking: #{sink.name}, Source Line: #{sink.source_line_num}, hasExtras=#{level}, hasRead=#{hasRead}, hasWrite=#{hasWrite}"
					puts text
					@all_warnings.push(text)

					vuln_increment("activityhijacking")
					vuln_increment("ah#{levelvalue}")
					
					if anyHasRead(sink)
						vuln_increment("flagRead")
					end
					if anyHasWrite(sink)
						vuln_increment("flagWrite")
					end

						
				end
				if sink.type=="startActivityForResult"
					if allHasChooser(sink)
						vuln_increment("activityhijackingresultChooser")
					else
						vuln_increment("activityhijackingresult")
					end
				end
			end
		when "service"
			if sink.type == "startService" || sink.type == "bindService"
				if checkIntentVulns(sink)
					hasRead=false
					hasWrite=false
					if anyHasRead(sink)
						vuln_increment("flagRead")
						hasRead=true
					end
					if anyHasWrite(sink)
						vuln_increment("flagWrite")
						hasWrite=true
					end
				
					level=anyHasExtra(sink)
					levelvalue=0
    			if level==true
    				levelvalue=1
    			end
					trackVulnIntents(sink.name)
					text = "Possible Service Hijacking: #{sink.name}, Source Line: #{sink.source_line_num}, hasExtras=#{level}, hasRead=#{hasRead}, hasWrite=#{hasWrite}"
					puts text
					@all_warnings.push(text)

					vuln_increment("servicehijacking")
					if(level)
						vuln_increment("sh#{levelvalue}")
					else
						vuln_increment("sh#{levelvalue}")
					end
					
					if sink.type=="bindService"
						vuln_increment("servicehijackingresult")
					end
				end
			end
		when "broadcast"
			if sink.permission != "" && hasStrongProtection(sink.permission) == true
				next;
			end
			level=anyHasExtra(sink)
			levelvalue=0
			if level==true
				levelvalue=1
			end
			vuln_increment("broadcastexposure")
			vuln_increment("be#{levelvalue}")
			
			hasRead=false
			hasWrite=false
			if anyHasRead(sink)
				vuln_increment("flagRead")
				hasRead=true
			end
			if anyHasWrite(sink)
				vuln_increment("flagWrite")
				hasWrite=true
			end

			trackVulnIntents(sink.name)
			case sink.type
			when "sendBroadcast"
				text = "Possible Broadcast Theft (Sniffing): #{sink.name}, Source Line: #{sink.source_line_num}, hasExtras=#{level}, hasRead=#{hasRead}, hasWrite=#{hasWrite}"
				puts text
				@all_warnings.push(text)

				vuln_increment("intentsniffing")
				vuln_increment("is#{levelvalue}")

			when "sendOrderedBroadcast"				
				text = "Possible Broadcast Theft (Sniffing, Intent theft, Result modification): #{sink.name}, Source Line: #{sink.source_line_num}, hasExtras=#{level}, hasRead=#{hasRead}, hasWrite=#{hasWrite}"
				puts text
				@all_warnings.push(text)

				vuln_increment("intentsniffing")
				vuln_increment("is#{levelvalue}")
				vuln_increment("intenttheft")
				vuln_increment("it#{levelvalue}")
				if sink.line=~/BroadcastReceiver/
					vuln_increment("broadcastresultmodification")
				end
			when "sendStickyBroadcast"
				text = "Possible Broadcast Theft (Sniffing, Intent theft, Result modification): #{sink.name}, Source Line: #{sink.source_line_num}, hasExtras=#{level}, hasRead=#{hasRead}, hasWrite=#{hasWrite}"
				puts text
				@all_warnings.push(text)
				vuln_increment("intentsniffing")
				vuln_increment("is#{levelvalue}")
				vuln_increment("intenttheft")
				vuln_increment("it#{levelvalue}")
			when "sendStickyOrderedBroadcast"
				text = "Possible Broadcast Theft (Sniffing, Intent theft, Result modification): #{sink.name}, Source Line: #{sink.source_line_num}, hasExtras=#{level}, hasRead=#{hasRead}, hasWrite=#{hasWrite}"
				puts text
				@all_warnings.push(text)
				vuln_increment("intentsniffing")
				vuln_increment("is#{levelvalue}")
				vuln_increment("intenttheft")
				vuln_increment("it#{levelvalue}")
				vuln_increment("broadcastresultmodification")
			else
				put "!!!BROADCAST NOT HANDLED!!!"
			end
		else
			puts "!!!Could not find sink type: #{sink.compType}"
		end
	end
	
end


def print_to_test_file(fileName, appname, componentName)
	File.open(fileName, 'a+') do |f|  
		 f.write("#{appname}\t#{componentName}\n")  
	end 
end

def findActionMisuse()
  actionMisuse = []
  componentsFound = []
  sinksFound = []
  @component_names.each do |name|
		component = @components[name]
		#if component.type != "dynamicreceiver"
			actions = component.actions
			actions.each do |action|
				if ! @knownAndroidIntents.include?(action)
					@sink_names.each do |sname|
						sink=@sinks[sname]
						if sink.done == true
							sink.intents.each do |intent|
								if ! intent.explicit && intent.action.include?(action)
									actionMisuse.push("Action Misuse: #{intent.dest_type} intent:{#{intent.name}} (at Source Line: #{sink.source_line_num}) to #{component.type} component:{#{component.name}} with {#{action}}")
									if ! componentsFound.include?(component.name)
										if @vuln_components.include?(component.name)
											componentsFound.push(component.name)
										end
									end
									if ! sinksFound.include?(sink.name)
										if @vuln_intents.include?(sink.name)
											sinksFound.push(sink.name)
										end
									end
								end
							end
						end
					end
				end
			end
		#end
	end

	File.open("#{@outfolder}actionMisuseCatchesWarnings", 'w') do |f|  
		f.write("#{componentsFound.length+sinksFound.length}\n")
	end

  printData("#{@outfolder}actionMisuse", actionMisuse.uniq.sort)
	@actionMisuseCount=actionMisuse.size
	@all_warnings =@all_warnings.concat(actionMisuse)
end

def findProtectedBroadcastVuln()
  protectedBroadcastVulns = []
  @component_names.each do |name|
		component = @components[name]
		if (component.type == "receiver") && component.visibility == true && (component.actions & @protected_Broadcasts).size >0
		  methods = @methods_for_class[component.name.split('*')[0]]
		  if methods != nil  #in case someone declares a component in the manifest that doesn't exist
		    vulnfound = true
		    methods.each do |meth|
		      code = @code[meth]
		      code.each do |line|
		        if line=~/^invoke-.*\s+\{(.*)\},android\/content\/Intent\/getAction/
		          vulnfound = false
		          break
		        end
		      end
		    end
		    if vulnfound == true
		      protectedBroadcastVulns.push("Protected System Broadcast w/o action check: #{component.type} component:{#{component.name}} does not check for {#{(component.actions & @protected_Broadcasts)}}")
		    end
		  end
    end
  end
  
  printData("#{@outfolder}protectedBroadcastNoAction", protectedBroadcastVulns.sort)
	
	@all_warnings =@all_warnings.concat(protectedBroadcastVulns)
end

def reduceRedundancies()
  @sink_names.each do |sname|
		sink=@sinks[sname]
		sink.intents.each do |intent|
		  intent.action = intent.action.uniq
		end
		sink.intents = sink.intents.uniq
	end
	
	@component_names.each do |name|
		component = @components[name]
    component.actions=component.actions.uniq
  end
end

def trackVulnComponents(name)
	@vuln_components.push(name)
end
def trackVulnIntents(name)
	@vuln_intents.push(name)
end

def printData(filename, array)
	File.open(filename, 'w') do |f|  
		array.each do |a|
			f.write("#{a}\n")
		end
	end
end

def actionStats(filedir)
	allActions={}
	totalImplicitIntents = 0
	implicitIntentsResolved = 0
	totalsinks = @sink_names.length
  actionArray=[]
  dynamicActions=[]
  
  sinksdone = 0
  sinksNotDone=[]
	@sink_names.each do |sname|
		sink=@sinks[sname]
		if sink.done == true
		  sinksdone += 1
			sink.intents.each do |intent|
				if ! intent.explicit
					intent.action.each do |action|
					  totalImplicitIntents += 1
					  if action != ""
					    implicitIntentsResolved += 1
					  end
						if allActions.has_key?(action)
							allActions[action] += 1
						else
							allActions[action] = 1
						end
						actionArray.push("#{action} #{intent.name}")
					end
				end
			end
		else
		  sinksNotDone.push(sname)
		end
	end

	actionArray=actionArray.sort

	@component_names.each do |name|
		component = @components[name]
		if component.type =="dynamicreceiver"
      component.actions.each do |action|
			  dynamicActions.push("#{action} #{component.name}")
			end
		end
	end

	printData("#{filedir}actionStats/actionFrequency", actionArray.sort)
	
	printData("#{filedir}actionStats/sinksNotDone.txt", sinksNotDone.sort)
	
	actionArray.insert(0, "#{totalImplicitIntents-implicitIntentsResolved} ActionsNotResolved",
	                      "#{totalImplicitIntents} TotalActions",
	                      "",
	                      "#{totalsinks-sinksdone} SinksNotFound",
                        "#{totalsinks} TotalSinks",
	                      "")
  actionArray.concat(dynamicActions.sort)

	printData("#{filedir}actionStats/actionDebug", actionArray)
	
	if totalImplicitIntents != implicitIntentsResolved
	  #$stderr.puts("NOT MATCHING")
	end

end

def stowawayOutput()
	activity_actions=[]
	broadcast_actions=[]
	service_actions=[]
	other_actions=[]

	@intent_names.each do |name|
		case @intents[name].dest_type
		when "activity"
			activity_actions.concat(@intents[name].action)
		when "Pactivity"
			activity_actions.concat(@intents[name].action)
		when "service"
			service_actions.concat(@intents[name].action)
		when "Pservice"
			service_actions.concat(@intents[name].action)
		when "broadcast"
			broadcast_actions.concat(@intents[name].action)
		when "Pbroadcast"
			broadcast_actions.concat(@intents[name].action)
		else
			other_actions.concat(@intents[name].action)
			if @intents[name].action.length != 0 					#only include if it has an action, don't include if it's a received action
				@other_action_location.push("#{name} #{@intents[name].action}")
			end
		end
	end

	puts "Activity actions"
	puts activity_actions.uniq
	puts
	puts "Broadcast actions"
	puts broadcast_actions.uniq
	puts
	puts "Service actions"
	puts service_actions.uniq
	puts
	puts "Other actions"
	puts other_actions.uniq
	puts
	puts "All actions (different technique)"
	puts @all_setActions.uniq
	puts

	
	all_dyn_actions=[]
	puts "Dynamic receiving actions"
	@intent_filters.keys.each do |actions|
		puts @intent_filters[actions]
		all_dyn_actions.concat(@intent_filters[actions])
	end
	
	banner("Other test:all strings")
	puts @all_strings.uniq.sort

  printData("#{@outfolder}sendActivityActions.txt", activity_actions.uniq)
  printData("#{@outfolder}sendBroadcastActions.txt", broadcast_actions.uniq)
  printData("#{@outfolder}sendServiceActions.txt", service_actions.uniq)
  printData("#{@outfolder}sendOtherActions.txt", other_actions.uniq)
  printData("#{@outfolder}otherActionLocation.txt", @other_action_location.uniq)
  
  printData("#{@outfolder}recvDynamicActions.txt", all_dyn_actions.uniq.sort)
  
  printData("#{@outfolder}allActions.txt", @all_setActions.uniq.sort)
  printData("#{@outfolder}allStrings.txt", @all_strings.uniq.sort)
  setActionNotFound.delete_if {|key, value| value==false }   
  printData("#{@outfolder}actionNotFound.txt", @setActionNotFound.keys.sort)
  
end

end


IA = IntentAnalysis.new
IA.main()
if $options[:comdroid]
  IA.find_component_vulnerabilities()
  IA.find_intent_vulnerabilities()
  IA.all_warnings=IA.all_warnings.uniq
  IA.findActionMisuse()
  IA.findProtectedBroadcastVuln()
  IA.logStats()
  IA.printData("#{IA.outfolder}allWarnings", IA.all_warnings.sort)
end

if $options[:stowaway]
  IA.stowawayOutput()                                     
end