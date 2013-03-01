#!/usr/bin/ruby

require 'optparse'
require 'ReflectObj'
require 'Register'
require 'FieldObj'


$appname= ""

$class_name  = ""
$class_super = ""
$source_file = ""


$in_method=false
$method_name = ""
$method_code =[]
$code = {}

$method_names = []

$line = nil
$line_num = ""	#line num with reference to source code
$line_count = ""  #line num with reference to method

$options = {}

$investigate_methods=[]
$method_returns_str={}
$method_returns_meth={}
$method_returns_cls={}
$method_returns_cons={}
$method_returns_obj={}

$reflect_names= []
$reflection= {}

$forNameUse=[]

#$vregisters = {}
#$acceptable_distance = 20

$num_found=0
$num_done=0
$obj_found=0
$outputdir=""

$count_newInstance = 0
$count_invoke = 0

$fields={}

$stringToClass={}

# verified by testing
$stringToClass['wifi']="android.net.wifi.WifiManager"
$stringToClass['window']="android.view.Window.LocalWindowManager"
$stringToClass['layout_inflater']="android.view.LayoutInflater"
$stringToClass['activity']="android.app.ActivityManager"
$stringToClass['power']="android.os.PowerManager"
$stringToClass['alarm']="android.app.AlarmManager"
$stringToClass['notification']="android.app.NotificationManager"
$stringToClass['keyguard']="android.app.KeyguardManager"
$stringToClass['location']="android.location.LocationManager"
$stringToClass['search']="android.app.SearchManager"
$stringToClass['vibrator']="android.os.Vibrator"
$stringToClass['input_method']="android.view.inputmethod.InputMethodManager"
$stringToClass['uimode']="android.app.UiModeManager"
$stringToClass['download']="android.app.DownloadManager"
$stringToClass['wimax']="com.htc.net.wimax.WimaxController"
$stringToClass['WiMax']="android.net.wimax.WimaxManager"
$stringToClass['phone']="android.telephony.TelephonyManager"
$stringToClass['audio']="android.media.AudioManager"
$stringToClass['wallpaper']="android.app.WallpaperManager"
$stringToClass['dropbox']="android.os.DropBoxManager"
$stringToClass['accessibility']="android.view.accessibility.AccessibilityManager"
$stringToClass['throttle']="android.net.ThrottleManager"
$stringToClass['connectivity']="android.net.ConnectivityManager"
$stringToClass['clipboard']="android.text.ClipboardManager"
$stringToClass['statusbar']="android.app.StatusBarManager"
$stringToClass['device_policy']="android.app.admin.DevicePolicyManager"
$stringToClass['sensor']="android.hardware.SensorManager"
$stringToClass['account']="android.accounts.AccountManager"

#substitutes; not present on N1? or hidden?
$stringToClass['iphonesubinfo']="com.android.internal.telephony.IPhoneSubInfo"
$stringToClass['simphonebook']="com.android.internal.telephony.IIccPhoneBook"
$stringToClass['isms']="com.android.internal.telephony.ISms"
$stringToClass['appwidget']="com.android.internal.appwidget.IAppWidgetService"
$stringToClass['backup']="android.app.backup.IBackupManager"
$stringToClass['mount']="android.os.storage.IMountService"
$stringToClass['network_management']="android.os.INetworkManagementService"
$stringToClass['netstat']="android.os.INetStatService"
$stringToClass['bluetooth_a2dp']="android.bluetooth.IBluetoothA2dp"
$stringToClass['hardware']="android.os.IHardwareService"
$stringToClass['content']="android.content.IContentService"
$stringToClass['permission']="android.os.IPermissionController"
$stringToClass['package']="android.content.pm.IPackageManager"
$stringToClass['telephony.registry']="com.android.internal.telephony.ITelephonyRegistry"
$stringToClass['usagestats']="com.android.internal.app.IUsageStats"
$stringToClass['batteryinfo']="com.android.internal.app.IBatteryStats"
$stringToClass['SurfaceFlinger']="android.ui.ISurfaceComposer"
$stringToClass['media.audio_policy']="android.media.IAudioPolicyService"
$stringToClass['media.camera']="android.hardware.ICameraService"
$stringToClass['media.player']="android.media.IMediaPlayerService"
$stringToClass['media.audio_flinger']="android.media.IAudioFlinger"
$stringToClass['bluetooth']="android.bluetooth.IBluetooth"

$classToService={}
$classToService['android.os.Vibrator']="android.os.IVibratorService"

$classToInterface={}

$allMethodsAndInits=[]
$investigate_methods1=[]
$investigate_methods2=[]
$investigate_methods3=[]
$methodcons_names= []
$methodcons= {}

$callGraph = {}
$reverseCallGraph = {}

$secondPassReflections =[]
######################################
def get_cmd_args()
		optparse = OptionParser.new do |opts|
				#opts.banner = "Usage: cfg.rb AppFileList1 AppFileList2 AppFileListN\n Where AppFileList is a return delimited file containing a fully qualified path on each line. To get a file list in a directory with *.ddx files use 'ls -1 $(pwd)/*.ddx'."

				opts.on( '-h', '--help', 'Display this screen' ) do
						puts opts
						exit
				end 

				$options[:verbose] = false
				opts.on("-v", "--[no-]verbose", "Run verbosely") do |v|
						$options[:verbose] = v
				end

				$options[:debug] = false
				opts.on("-y","--debug", "Debug info") do
				    $options[:debug] = true
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
		$method_name = ""
		$method_code = []
		$in_method = false
		$line_count = 0
end

################Utils

#format: a/b/c()
def canonicalize_method_name(method)
		path = ""
		if ($class_name.split(' ').size == 1 ) then
			path = $class_name	
		else
			sr = $class_name.split(' ')
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
	return $code[method]
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

def vuln_increment(type)
	$vulnerabilities[type]= $vulnerabilities[type]+1
end

def hasStrongProtection(perm)
	if !$protection_levels.has_key?(perm)
		puts "!!!Permission level for permission check not found: #{perm}"
		return false
	end
	return $protection_levels[perm] >= 3
end
#################
def record_methods(fn)
	f = File.new(fn)
	begin
		while ($line = f.readline)
			parse_for_method($line)
		end
	rescue EOFError
		f.close
	end
end

def parse_for_method(line)
	if (/\S/ !~ line) then 
		return
	end
	
	if ($in_method == true) then
		$method_code.push(line.strip)
		$line_count= $line_count+1
	end
    
  if ($in_method == true) then
    if (line.strip =~ /^invoke-\S+\s+\{.*\},(\S+)\s*;.*(\(.*\))/)
      call= $1
      params=$2
      if ((!call.start_with?("android.") && !call.start_with?("java.")))
        if $callGraph.has_key?($method_name)
          $callGraph[$method_name] = $callGraph[$method_name].push("#{call}#{params}")
        else
          $callGraph[$method_name] = ["#{call}#{params}"]
        end
      end
    end
  end
    
	if (line.strip =~ /^\.(class|super|source|field|method|limit|line|end|inner|implements|annotation|interface) (.*)/) then
		handle_line(line.strip, $1, $2)
	elsif (line.strip =~ /^invoke-virtual.*\{.*\},java\/lang\/reflect\/Method\/invoke\s*;/)
		puts "Found method invocation"
		#$investigate_methods.push($method_name)
		$count_invoke+=1
		record_reflection(line, "invoke")
	elsif (line.strip =~ /^invoke-virtual.*\{.*\},java\/lang\/reflect\/Constructor\/newInstance\s*;/)
		puts "Constructor invocation"
		#$investigate_methods.push($method_name)
		$count_newInstance+=1
		record_reflection(line, "newInstance")
	elsif (line.strip =~/^invoke-static.*\{.*\},java\/lang\/Class\/forName\s*;/)
		$investigate_methods.push($method_name)
	elsif (line.strip =~ /^invoke-virtual.*\{.*\},java\/lang\/Class\/(getDeclaredMethod|getMethod)\s*;/)
		record_MethConsUse(line, "method")
		$investigate_methods2.push($method_name)
	elsif (line.strip =~ /^invoke-virtual.*\{.*\},java\/lang\/Class\/(getDeclaredConstructor|getConstructor)\s*;/)
		record_MethConsUse(line, "constructor")
		$investigate_methods2.push($method_name)
	end
end

def record_MethConsUse(line, type)
	a = ReflectObj.new($method_name, $line_count, line, type)
	#a.source_line_num=$line_num
	puts "Method/Cons: #{a.name}" if $options[:verbose]
	a.type = type
	$methodcons_names.push(a.name)
	$methodcons[a.name]=a
end

def record_reflection(line, type)
	a = ReflectObj.new($method_name, $line_count, line, type)
	#a.source_line_num=$line_num
	puts "Reflection: #{a.name}" if $options[:verbose]
	a.type = type
	$reflect_names.push(a.name)
	$reflection[a.name]=a
end

def print_reflections()
	$num_found=0
	$num_done=0
	$obj_found=0
	$num_classUnknown=0
	$total_reflects = 0
	$sinks_found = 0
	$reflect_names.each do |name|
		puts "#{name}: #{$reflection[name].done}"
		if $reflection[name].done
			$num_done+=1
		end
		if $reflection[name].classUnknown
			$num_classUnknown+=1
		end
		
    if $reflection[name].found
  		$sinks_found+=1
  	end

	  puts "  #{$reflection[name].dest}"
		$reflection[name].calledDests.keys.each do |path|
		  dests = $reflection[name].calledDests[path]
      dests.each do |dest|
        puts "  #{dest}"
      end
		end
		
		if $reflection[name].dest.include?("java/lang/Object/") || $reflection[name].dest.include?("java.lang.Object.")
		  $obj_found+=1
		end
		
		if !isReflectionResolutionUnsucessful($reflection[name].dest)
		  $num_found+=1
		  $total_reflects+=1
		elsif $reflection[name].calledDests.keys.length != 0
		  $reflection[name].calledDests.keys.each do |path|
		    dests = $reflection[name].calledDests[path]
        dests.each do |dest|
          if !isReflectionResolutionUnsucessful(dest)
            $num_found+=1
		        $total_reflects+=1
		      else
		        $total_reflects+=1
		      end
		      if dest.include?("java/lang/Object/") || dest.include?("java.lang.Object.")
			      $obj_found+=1
		      end
		    end
		  end
		else
		  $total_reflects+=1
	  end
	end
	
	$methodconsfull_count=0
	$methodconstotal=0
	$methodcons_names.each do |name|
	  $methodcons[name].calledDests.keys.each do |path|
	    dests = $methodcons[name].calledDests[path]
      dests.each do |dest|
		    if isReflectionResolutionUnsucessful(dest)
			    $methodconsfull_count+=1
		    end
		    $methodconstotal+=1
	    end
	    if isReflectionResolutionUnsucessful($methodcons[name].dest)
		    $methodconsfull_count+=1
	    end
	    $methodconstotal+=1
	  end
	end
	
	counts={}
	counts['numfound']=$num_found
	counts['numnotfound']=$total_reflects-$num_found
	counts['objfound']=$obj_found
	counts['totalpossible']=$total_reflects

  counts['sinksfound']=$sinks_found
	counts['numclassunknown']=$num_classUnknown
	counts['numdone']=$num_done
	counts['totalsinks']=$count_newInstance+$count_invoke

	counts['nummethodconsfull']=$methodconsfull_count


	puts "Num Found: #{counts['numfound']}"
	puts "Num Not Found: #{counts['numnotfound']}"
	puts "Num Object: #{counts['objfound']}"
	puts "Total possible: counts['totalpossible']"
	puts "***"
	puts "Num Class Unknown: #{counts['numclassunknown']}"
	puts "Num Done: #{counts['numdone']}"
	puts "Sinks Found: #{counts['sinksfound']}"
	puts "Total: #{counts['totalsinks']}"

	
	File.open("#{$outputdir}count", 'w+') do |f|
		f.write("numfound #{counts['numfound']}\n")
		f.write("numnotfound #{counts['numnotfound']}\n")
		f.write("objfound #{counts['objfound']}\n")
		f.write("totalpossible #{counts['totalpossible']}\n")

		f.write("numclassunknown #{counts['numclassunknown']}\n")
		f.write("numdone #{counts['numdone']}\n")
    f.write("sinksfound #{counts['sinksfound']}\n")
		f.write("totalsinks #{counts['totalsinks']}\n")

		f.write("nummethodconsfull #{counts['nummethodconsfull']}\n")
		f.write("nummethodconstotal #{$methodconstotal}\n")
	end 

end


def handle_line(line, directive, data)
	case directive
	when "class"
			$class_name = data.split(' ').last
	when "super"
			$class_super = data
	when "source"
			$source_file = data
	when "field"
			parsed = line.strip.split('=')
			fieldinfo = parsed[0].strip.split(' ')
			type=fieldinfo[-1].delete(';')
			#if type.start_with?('L')
			#	type=type[1..-1]
			#end
			name=fieldinfo[-2]
			a = FieldObj.new(name, $class_name, type)
			if parsed.size>1 && parsed[1].include?("\"")
				value = parsed[1].strip.delete('\"')
				a.value=value
				#puts value
			end
			$fields[a.name] = a
			#puts "Adding #{a.name}, #{name}"
	when "method"
			$line_count = 0
			$in_method = true
			$method_code.push(line.strip)
			$method_name = canonicalize_method_name(data)
			$method_names.push($method_name)
			#$methods_in_class.push($method_name)
			if $method_name.include?("<clinit>()")
				$investigate_methods1.push($method_name)
			elsif $method_name.include?("<init>")
				$investigate_methods1.push($method_name)
			elsif $method_name.include?("onCreate")
  			$investigate_methods3.push($method_name)
			end

			if(line.strip =~ /.*\)Ljava\/lang\/String;/)
				$method_returns_str[$method_name]=""
			elsif(line.strip =~ /.*\)Ljava\/lang\/reflect\/Method;/)
				$method_returns_meth[$method_name]=""
			elsif(line.strip =~ /.*\)Ljava\/lang\/reflect\/Constructor;/)
				$method_returns_cons[$method_name]=""
			elsif(line.strip =~ /.*\)Ljava\/lang\/Class;/)
				$method_returns_cls[$method_name]=""
			elsif(line.strip =~ /.*\)Ljava\/lang\/Object;/)
				$method_returns_obj[$method_name]=""
			end

	when "limit"
			#nothing
	when "inner"

	when "implements"

	when "annotation"

	when "line"
			$line_num = data
	when "end"
			if data.strip == "method" then
				save_method_code()
			end
	when "interface"
		$class_name = data.split(' ').last
	end
end

def save_method_code()
		#Adding method code for the method code table
		$code[$method_name]=$method_code
		reset()
end

def look_for_values(method, code, first, params, path)
	puts "Starting another run #{method} #{first.to_s}"
	puts "Num of params: #{params.length}, Param values: #{params.join(", ")}"
	vregisters={}
	$line_num=-1
	code.each_with_index.each() do |line, i|
		case line
		when /^.line\s+(\d+)/
			$line_num = $1
			#puts "LINE: #{$line_num}"
		when /^;\s+parameter\[(\d+)\]\s+:\s+(v\d+)\s+\(Ljava\/lang\/reflect\/Method;\)/
			place = $1.to_i
			if (first!=0 && params != [] && params[place] != nil)
				recordRegister($2, "method", params[place], vregisters)
				puts "method: #{params[place]} Param, #{$2}"  #if $options[:debug]
			else
				recordRegister($2, "method", "**unknownMethodParam", vregisters)
				puts "method: unknownMethodParam, #{$2}"  #if $options[:debug]
			end
		when /^;\s+parameter\[(\d+)\]\s+:\s+(v\d+)\s+\(Ljava\/lang\/Class;\)/
			place = $1.to_i
			if ( (first!=0) && params != [])
				#puts "HI #{params[place]}"
				recordRegister($2, "class", params[place], vregisters)
				puts "class: #{params[place]} Param, #{$2}"  #if $options[:debug]
			else
				recordRegister($2, "class", "**unknownClassParam", vregisters)
				puts "class: unknownClassParam, #{$2}"  #if $options[:debug]
			end
		when /^;\s+parameter\[(\d+)\]\s+:\s+(v\d+)\s+\(Ljava\/lang\/String;\)/
			place = $1.to_i
			if ((first!=0) && params != [])
				recordRegister($2, "string", params[place], vregisters)
				puts "string: #{params[place]} Param, #{$2}"  #if $options[:debug]
			else
				recordRegister($2, "string", "**unknownStringParam", vregisters)
				puts "string: unknownStringParam, #{$2}"  #if $options[:debug]
			end
		when /^;\s+parameter\[(\d+)\]\s+:\s+(v\d+)\s+\(Ljava\/lang\/Object;\)/
			place = $1.to_i
			if ((first!=0) && params != [])
				recordRegister($2, "object", params[place], vregisters)
				puts "object: #{params[place]} Param, #{$2}"  #if $options[:debug]
			else
				recordRegister($2, "object", "**unknownObjectParam", vregisters)
				puts "object: unknownObjectParam, #{$2}"  #if $options[:debug]
			end
		when /^const-(string)\s+(v[0-9]+),\"(.*)\"/
			recordRegister($2, $1, $3, vregisters)
			puts "string: #{$3}, #{$2}"  #if $options[:debug]
			vregisters[$2].isOrigConst = true
		when /^const-(class)\s+(v[0-9]+),(.*)/
			recordRegister($2, $1, $3, vregisters)
			puts "class: #{$3}, #{$2}"  #if $options[:debug]
		when /^const\/4\s+(v[0-9]+),(.*)/
  		recordRegister($1, "num", $2, vregisters)
  		puts "num: #{$2}, #{$1}"  #if $options[:debug]
		when /^const-\S+\s+(v[0-9]+),.*/
			removeRegister($1, vregisters)
			puts "clearing: #{$1}"  #if $options[:debug]
		when /^check-cast\s+(v[0-9]+),(.*)/
			reg=$1
			type=$2
			if correctRegisterType(reg, "object", vregisters)
				recordRegister(reg, "object",  type, vregisters)
			end
			puts "Found check-cast #{type}"
			
		when /^invoke-virtual.*\{.*\},java\/lang\/Object\/getClass\s*;/
			reg = get_register(line, 0)
			secondline = code[i+1]
			classvalue = get_comment_type(secondline, reg)
			return_reg = find_return_register(code, i)
			if classvalue == "Ljava/lang/Object"
				if correctRegisterType(reg, "object", vregisters)
					classvalue = vregisters[reg].value
				#elsif hasRegisterType(reg, vregisters)
				#	classvalue = vregisters[reg].value.concat("?")
				end
			end
			recordRegister(return_reg, "class", classvalue, vregisters)
			puts "class: #{classvalue}, #{return_reg}"
			
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
			
		when /^invoke-.*\{.*\},java\/lang\/Class\/(getSimpleName|getName)\s*;/
			reg = get_register(line, 0)
			if correctRegisterType(reg, "class", vregisters)
				return_reg = find_return_register(code, i)
				recordRegister(return_reg, "string", vregisters[reg].value, vregisters)
				puts "string: #{vregisters[reg].value}, #{return_reg}"
			end

    when /^invoke-.*\{.*\},java\/lang\/reflect\/Method\/(getName)\s*;/
			reg = get_register(line, 0)
			if correctRegisterType(reg, "method", vregisters)
				return_reg = find_return_register(code, i)
				name = vregisters[reg].value
				if name =~/(.*)\*\*unknownMethod/
				  name = "#{$1}**unknownGetName*#{reg}*"
				else 
				  puts("ASDF")
				end
				recordRegister(return_reg, "string", name, vregisters)
				puts "string: (getName) #{name}, #{return_reg}"
				vregisters[return_reg].from = reg
			else
			  return_reg = find_return_register(code, i)
				recordRegister(return_reg, "string", "**unknownGetName*#{reg}*", vregisters)
				puts "string: (getName) **unknownGetName*#{reg}*, #{return_reg}"
			end

		when /^invoke-.*\{.*\},java\/lang\/StringBuilder\/<init>.*(\(.*\)).*/
			params = $1
			case params
			when "()", "(Z)"
				reg = get_register(line, 0)
				recordRegister(reg, "stringbuilder", "", vregisters)
				puts "stringbuilder: #{vregisters[reg].value}, #{reg}"
			when "(Ljava/lang/String;)"
				reg = get_register(line, 0)
				reg1 = get_register(line, 1)
				if correctRegisterType(reg1, "string", vregisters)
					recordRegister(reg, "stringbuilder",  vregisters[reg1].value, vregisters)
					puts "stringbuilder: #{vregisters[reg].value}, #{reg}"
				end
			#when CHARSEQUENCE
			end
		when /^invoke-.*\{.*\},java\/lang\/StringBuilder\/append.*(\(.*\)).*/
			params = $1
			case params
			when "(Ljava/lang/String;)"
				reg = get_register(line, 0)
				reg1 = get_register(line, 1)
				if correctRegisterType(reg1, "string", vregisters) && correctRegisterType(reg, "stringbuilder", vregisters)
					return_reg = find_return_register(code, i)
					if return_reg != "-1"
						recordRegister(return_reg, "stringbuilder",  "#{vregisters[reg].value}#{vregisters[reg1].value}", vregisters)
						puts "stringbuilder: #{vregisters[return_reg].value}, #{return_reg}"
						if return_reg != reg
							recordRegister(reg, "stringbuilder",  vregisters[return_reg].value, vregisters)
						end
					else
						recordRegister(reg, "stringbuilder", "#{vregisters[reg].value}#{vregisters[reg1].value}", vregisters)
						puts "stringbuilder: #{vregisters[reg].value}, #{reg}"
					end
				end
			else
				reg = get_register(line, 0)
				if correctRegisterType(reg, "stringbuilder", vregisters)
					return_reg = find_return_register(code, i)
					if return_reg != "-1"
						recordRegister(return_reg, "stringbuilder",  "#{vregisters[reg].value}?", vregisters)
						puts "stringbuilder: #{vregisters[return_reg].value}, #{return_reg}"
						if return_reg != reg
							recordRegister(reg, "stringbuilder",  vregisters[return_reg].value, vregisters)
						end
					else
						recordRegister(reg, "stringbuilder",  "#{vregisters[reg].value}?", vregisters)
						puts "stringbuilder: #{vregisters[reg].value}, #{reg}"
					end
				end
			end
		when /^invoke-.*\{.*\},java\/lang\/StringBuilder\/toString\s*;/
			reg = get_register(line, 0)
			if correctRegisterType(reg, "stringbuilder", vregisters)
				return_reg = find_return_register(code, i)
				recordRegister(return_reg, "string",  vregisters[reg].value, vregisters)
				puts "string: #{vregisters[return_reg].value}, #{return_reg}"
			end

    when /^invoke-.*\{.*\},java\/lang\/String\/(equals|equalsIgnoreCase)\s*;/
      reg1 = get_register(line, 0)
      reg2 = get_register(line, 1)
      if correctRegisterType(reg1, "string", vregisters) && correctRegisterType(reg2, "string", vregisters)
        if vregisters[reg1].isOrigConst && vregisters[reg2].from=~/v\d+/
          val="**unknownMethod"
          call = vregisters[reg2].value.split("/").join(".").split(".")
          if call.length >1 
            val=vregisters[reg2].value
          elsif correctRegisterType(vregisters[reg2].from, "method", vregisters)
            val=vregisters[vregisters[reg2].from].value
          end
          temp=combinePackageAndMethod(vregisters[reg1].value, val)
          puts "Encountered equals: #{vregisters[reg1].value}, #{val}, to #{temp} "
          recordRegister(vregisters[reg2].from, "method", temp, vregisters)
          puts "method: (going back and filling) #{temp}, #{vregisters[reg2].from}"
          recordRegister(reg2, "string",  temp, vregisters)
          puts "string: (equals) #{temp}, #{reg2}"
        elsif vregisters[reg2].isOrigConst && vregisters[reg1].from=~/v\d+/
          val="**unknownMethod"
          call = vregisters[reg1].value.split("/").join(".").split(".")
          if call.length >1 
            val=vregisters[reg1].value
          elsif correctRegisterType(vregisters[reg1].from, "method", vregisters)
            val=vregisters[vregisters[reg1].from].value
          end
          temp=combinePackageAndMethod(vregisters[reg2].value, val)
          puts "Encountered equals1: #{vregisters[reg2].value}, #{val}, to #{temp} "
          recordRegister(vregisters[reg1].from, "method", temp, vregisters)
          puts "method: (going back and filling) #{temp}, #{vregisters[reg1].from}"
          recordRegister(reg1, "string",  temp, vregisters)
          puts "string: (equals) #{temp}, #{reg1}"
        else
          puts "Encountered String/equals but did nothing1"
        end
      else
        puts "Encountered String/equals but did nothing2"
  		end
  		
		when /^sput-object\s+(v[0-9]+),(.*) (.*)/
			reg = $1
			param = $2
			type = $3
			if vregisters.has_key?(reg)
				if $fields.has_key?(param)
				  if vregisters[reg].value.include?("**unknown") &&  !($fields[param].value.include?("**unknown") || $fields[param].value == "")
				    puts "Not Saving #{vregisters[reg].value} to #{param} because it has '#{$fields[param].value}'"
				  else
					  $fields[param].value = vregisters[reg].value
					  puts "Saving #{vregisters[reg].value} to #{param}"
					end
				else
					puts "!!!!!COULD NOT FIND FIELD KEY: #{param}"
				end
			end
		when /^sget-object\s+(v[0-9]+),(.*) (.*)/
			reg = $1
			param = $2
			type = $3
			if $fields.has_key?(param)
				value = $fields[param].value
				if value ==""
					value = "**unknown"
				end
				puts "Loading #{value} from #{param} to #{reg}"
				#must have semicolon in end
				case type
				when "Ljava/lang/reflect/Method;"
					recordRegister(reg, "method", value, vregisters)
				when "Ljava/lang/Class;"
					recordRegister(reg, "class", value, vregisters)
				when "Ljava/lang/String;"
					recordRegister(reg, "string", value, vregisters)
				when "Ljava/lang/reflect/Constructor;"
					recordRegister(reg, "constructor", value, vregisters)
				when "Ljava/lang/Object;"
					recordRegister(reg, "object", value, vregisters)
				when "[Ljava/lang/Class;"
  				recordRegister(reg, "classArray", value, vregisters)
  			else
				  puts "  Loading #{$fields[param].getType()} instead"
					recordRegister(reg, "object", $fields[param].getType(), vregisters)
				end
			end
			
		when /^iput-object\s+(v[0-9]+),(v[0-9]+),(.*) (Ljava\/lang\/Object|Ljava\/lang\/reflect\/Method|Ljava\/lang\/Class|Ljava\/lang\/String|Ljava\/lang\/reflect\/Constructor)/
			reg = $1
			ignore = $2			#we are treating this as a static var,
			param = $3
			if vregisters.has_key?(reg) && !correctRegisterType(reg, "num", vregisters)
				if $fields.has_key?(param)
					$fields[param].value = vregisters[reg].value
					puts "Saving #{vregisters[reg].value} to #{param}"
				else
					puts "!!!!!COULD NOT FIND FIELD KEY: #{param}"
				end
			else
			  puts "Not putting number into this field"
			end

		when /^iget-object\s+(v[0-9]+),(v[0-9]+),(.*) (Ljava\/lang\/Object|Ljava\/lang\/reflect\/Method|Ljava\/lang\/Class|Ljava\/lang\/String|Ljava\/lang\/reflect\/Constructor)/
			reg = $1
			ignore = $2
			param = $3
			type = $4
			if $fields.has_key?(param)
				value = $fields[param].value
				if value ==""
					value = "**unknown"
				end
				puts "Loading #{value} from #{param} to #{reg}"
				#must not have semicolon in end
				case type
				when "Ljava/lang/reflect/Method"
					recordRegister(reg, "method", value, vregisters)
				when "Ljava/lang/Class"
					recordRegister(reg, "class", value, vregisters)
				when "Ljava/lang/String"
					recordRegister(reg, "string", value, vregisters)
				when "Ljava/lang/reflect/Constructor"
					recordRegister(reg, "constructor", value, vregisters)
				when "Ljava/lang/Object"
					recordRegister(reg, "object", value, vregisters)
				else
  				puts "  Loading #{$fields[param].getType()} instead"
					recordRegister(reg, "object", $fields[param].getType(), vregisters)
				end
			end
			
			
		

		#when /^new-instance\s+(v[0-9]+),/
		#	removeRegister($1)
		when /^move-object.*(v[0-9]+),(v[0-9]+)/
			reg1=$1
			reg2=$2
			if vregisters.has_key?(reg2)
				recordRegister(reg1, vregisters[reg2].getType, vregisters[reg2].value, vregisters)
				vregisters[reg1].copyLinks(vregisters[reg2])
				vregisters[reg2].addLink(reg1)
				vregisters[reg1].addLink(reg2)
				puts "Update Reg: #{vregisters[reg1].name} #{vregisters[reg1].getType} #{vregisters[reg1].value}" if $options[:debug]
			elsif vregisters.has_key?(reg1) && !vregisters.has_key?(reg2) 
				puts "Deleting Reg: #{vregisters[reg1].name}"  if $options[:debug]
				vregisters.delete(reg1)
			end
		when /^invoke-static.*\{.*\},java\/lang\/Class\/forName\s*;/
			reg = get_register(line, 0)
			if correctRegisterType(reg, "string", vregisters)
				$forNameUse.push(vregisters[reg].value)
				return_reg = find_return_register(code, i)
				
				if return_reg != "-1"
					recordRegister(return_reg, "class", vregisters[reg].value, vregisters)
					puts "Found forName class: #{vregisters[reg].value}"
				else
					puts "Could not find return register value"
				end
			else
				puts "Incorrect type"
			end
		when /^invoke-virtual.*\{.*\},java\/lang\/Class\/(getDeclaredMethod|getMethod)\s*;/
			reg = get_register(line, 0)
			className="**unknownClass"
			if correctRegisterType(reg, "class", vregisters)
				className=vregisters[reg].value
			end
			methodname_reg = get_register(line, 1)
			methodname ="**unknownMethod"
			if correctRegisterType(methodname_reg, "string", vregisters)
				methodname = vregisters[methodname_reg].value
			end
			return_reg = find_return_register(code, i)
			if return_reg != "-1"
				recordRegister(return_reg, "method", "#{className}/#{methodname}", vregisters)
				puts "Found get[Declared]Method class: #{className}/#{methodname}"
				methcons=$methodcons["#{method}@#{i.to_s}"]
				methcons.done=true
				if first==0
				  methcons.dest = "#{className}/#{methodname}"
				else
				  methcons.calledDests[path] = set_called_dests(methcons, path, "#{className}/#{methodname}")    
				end
			else
				puts "Could not find return register value"
			end
			
			
		when /^invoke-virtual.*\{.*\},java\/lang\/Class\/(getDeclaredMethods|getMethods)\s*;/
			reg = get_register(line, 0)
			className="**unknownClass"
			if correctRegisterType(reg, "class", vregisters)
				className=vregisters[reg].value
			end
			return_reg = find_return_register(code, i)
			if return_reg != "-1"
				recordRegister(return_reg, "methodArray", "#{className}", vregisters)
				puts "Found get[Declared]Method*S* class: #{className}, #{return_reg}"
			else
				puts "Could not find return register value"
			end
		
		when /^aget-object\s+(v\d+),(v\d+),(v\d+)/
		  srcReg = $2
		  destReg = $1
		  if correctRegisterType(srcReg, "methodArray", vregisters)
		    puts "Method from MethodArray: #{vregisters[srcReg].value}/**unknownMethod, #{destReg}"
		    recordRegister(destReg, "method", "#{vregisters[srcReg].value}/**unknownMethod", vregisters)
		    vregisters[destReg].from = srcReg  			
		  elsif correctRegisterType(srcReg, "consArray", vregisters)
		    puts "Constructor from consArray: #{vregisters[srcReg].value}, #{destReg}"
		    recordRegister(destReg, "constructor", vregisters[srcReg].value, vregisters)
		    vregisters[destReg].from = srcReg
		  elsif correctRegisterType(srcReg, "method", vregisters)
  		  puts "Method from MethodArray is already Method: #{vregisters[srcReg].value}, #{destReg}"
  		  recordRegister(destReg, "method", "#{vregisters[srcReg].value}", vregisters)
  		else
  		  puts "Skipping aget-object"
			end

		when /^aput-object\s+(v\d+),(v\d+),(v\d+)/
		  srcReg = $1
		  destReg = $2

		  varType = get_comment_type(code[i+1], srcReg)
		  if varType =="Ljava/lang/reflect/Method"
		    varType = "method"
			elsif varType == "Ljava/lang/Class"
				varType="class"
			elsif varType == "Ljava/lang/String"
				varType="string"
			elsif varType == "Ljava/lang/reflect/Constructor"
				varType="constructor"
			elsif varType == "Ljava/lang/Object"
				varType="object"
			end
		  if correctRegisterType(srcReg, varType, vregisters)
		    value = vregisters[srcReg].value
		    case varType
			  when "method"
			    puts("Adding #{varType}Array with value #{value}, #{destReg}")
				  recordRegister(destReg, "methodArray", value, vregisters)
			  when "class"
  		    puts("Adding #{varType}Array with value #{value}, #{destReg}")
				  recordRegister(destReg, "classArray", value, vregisters)
			  when "string"
  		    puts("Adding #{varType}Array with value #{value}, #{destReg}")
				  recordRegister(destReg, "stringArray", value, vregisters)
			  when "constructor"
  		    puts("Adding #{varType}Array with value #{value}, #{destReg}")
				  recordRegister(destReg, "consArray", value, vregisters)
			  when "object"
  		    puts("Adding #{varType}Array with value #{value}, #{destReg}")
				  recordRegister(destReg, "objectArray", value, vregisters)
				else
				  puts("Not handling this type of aput-object")
        end
      else
        puts "Skipping aput-object"
      end
      
		when /^invoke-virtual.*\{.*\},java\/lang\/Class\/(getDeclaredConstructors|getConstructors)\s*;/
			reg = get_register(line, 0)
			className="**unknownClass"
			if correctRegisterType(reg, "class", vregisters)
				className=vregisters[reg].value
			end
			return_reg = find_return_register(code, i)
			if return_reg != "-1"
				recordRegister(return_reg, "consArray", "#{className}/<init>", vregisters)
				puts "Found get[Declared]Cons*S* class: #{className}/<init>"
			else
				puts "Could not find return register value"
			end

			
		when /^invoke-virtual.*\{.*\},java\/lang\/Class\/(getDeclaredConstructor|getConstructor)\s*;/
			reg = get_register(line, 0)
			className="**unknownClass"
			if correctRegisterType(reg, "class", vregisters)
				className=vregisters[reg].value
			end
			return_reg = find_return_register(code, i)
			if return_reg != "-1"
				puts "Found get[Declared]Constructor class: #{className}/<init>"
				recordRegister(return_reg, "constructor", "#{className}/<init>", vregisters)
				methcons=$methodcons["#{method}@#{i.to_s}"]
				methcons.done=true
				if first==0
				  methcons.dest = "#{vregisters[return_reg].value}"
			  else		    
			    methcons.calledDests[path] = set_called_dests(methcons, path, vregisters[return_reg].value)
  			end
			else
				puts "Could not find return register value"
			end
		when /^invoke-virtual.*\{.*\},java\/lang\/Class\/(getDeclaredField|getField)\s*;/
			reg = get_register(line, 0)
			if correctRegisterType(reg, "class", vregisters)
				className=vregisters[reg].value.split("/").join(".")
				if className.start_with?('L')
					className=className[1..-1]
				end

				reg2 = get_register(line, 1)
				if correctRegisterType(reg2, "string", vregisters) && vregisters[reg2].value == "mService" && $classToService.has_key?(className)
					return_reg = find_return_register(code, i)
					if return_reg != "-1"
						recordRegister(return_reg, "object", "#{$classToService[className]}", vregisters)
						puts "Found get[Declared]Field class: #{$classToService[className]}"
					else
						puts "Could not find return register value"
					end
				else
					#puts "#{vregisters[reg2].value} #{className} #{$classToService.has_key?(className)}"
				end
			end
			
		when /^invoke-virtual.*\{.*\},java\/lang\/reflect\/Field\/get\s*;/
			reg = get_register(line, 0)
			if correctRegisterType(reg, "object", vregisters)
				objName=vregisters[reg].value
				return_reg = find_return_register(code, i)
				if return_reg != "-1"
					recordRegister(return_reg, "object", "#{objName}", vregisters)
					puts "Found Field get: #{objName}"
				else
					puts "Could not find return register value"
				end
			end

		when /^invoke-virtual.*\{.*\},java\/lang\/reflect\/Method\/invoke\s*;/
			reg = get_register(line, 0)
			if correctRegisterType(reg, "method", vregisters)
				reflect=$reflection["#{method}@#{i.to_s}"]
				#if (not reflect.done or vregisters[reg].value=~ /\*\*unknown/)
					reflect.done=true
					if first==0
  				  reflect.dest = vregisters[reg].value
  				else
  				  reflect.calledDests[path] = set_called_dests(reflect, path, vregisters[reg].value)
  				end
					puts "Found reflection in #{method}, src_line:#{$line_num}, ddx_line:#{i}; #{vregisters[reg].value}" #if $options[:verbose]
					if !isReflectionResolutionUnsucessful(vregisters[reg].value)
						reflect.found = true
					end
					classAndMethod = vregisters[reg].value.split("/")
					if classAndMethod.length == 1
						reflect.classUnknown = true
					else
						tmp = classAndMethod[0..-2].join("/")
						if tmp.include?("**unknown") || tmp.include?("java.lang.Object") || tmp.include?("java/lang/Object")
							reflect.classUnknown = true
						end
					end
				#end
				
				return_reg = find_return_register(code, i)
				if return_reg != "-1"
					splitpath = vregisters[reg].value.split("/")
					methodCalled = vregisters[reg].value.split("/").join(".")
					if methodCalled.start_with?('L')
						methodCalled=methodCalled[1..-1]
					end
					classval = splitpath[0..-2].join("/")
					if classval.include?("$Stub")
					  puts "Object: #{classval.split("$Stub")[0]}, #{return_reg}"
						recordRegister(return_reg, "object", classval.split("$Stub")[0], vregisters)
					elsif $classToInterface.has_key?(methodCalled)
					  puts "Object: #{$classToInterface[methodCalled]}, #{return_reg}"
						recordRegister(return_reg, "object", $classToInterface[methodCalled], vregisters)
					else
					  puts "Object: #{classval}, #{return_reg}"
						recordRegister(return_reg, "object", classval, vregisters)
					end
				end
			else
				puts "!!!Method type not found: #{method}, #{i}"
			end
		when /^invoke-virtual.*\{.*\},java\/lang\/reflect\/Constructor\/newInstance\s*;/
			reg = get_register(line, 0)
			if correctRegisterType(reg, "constructor", vregisters)
				reflect=$reflection["#{method}@#{i.to_s}"]
				#if (not reflect.done or vregisters[reg].value=~ /\*\*unknown/)
					reflect.done=true
					if first==0
            reflect.dest = vregisters[reg].value
          else
  				  reflect.calledDests[path] = set_called_dests(reflect, path, vregisters[reg].value)
          end
					puts "Found reflection, src_line:#{$line_num}, ddx_line:#{i}" #if $options[:verbose]
					if !isReflectionResolutionUnsucessful(vregisters[reg].value)
						reflect.found = true
					end

					classAndMethod =  vregisters[reg].value.split("/")
					if classAndMethod.length == 1
						reflect.classUnknown = true
					else
						tmp = classAndMethod[0..-2].join("/")
						if tmp.include?("**unknown") || tmp.include?("java.lang.Object") || tmp.include?("java/lang/Object")
							reflect.classUnknown = true
						end
					end
				#end
				
				return_reg = find_return_register(code, i)
				if return_reg != "-1"
					splitpath = vregisters[reg].value.split("/")
					classval = splitpath[0..-2].join("/")
					recordRegister(return_reg, "object", classval, vregisters)
				end
			else
				puts "!!!Constructor type not found: #{method}, #{i}"
			end

		#when you change this make the corresponding change in the other getSystemService block
		when /^invoke-virtual.*\{.*\},android\/content\/Context\/getSystemService\s*;/
			reg = get_register(line, 1)
			if correctRegisterType(reg, "string", vregisters)
				puts vregisters[reg].value
				if $stringToClass.has_key?(vregisters[reg].value)
					return_reg = find_return_register(code, i)
          puts "object: systemService #{vregisters[reg].value} -> #{$stringToClass[vregisters[reg].value]}, #{return_reg}"
					recordRegister(return_reg, "object", $stringToClass[vregisters[reg].value], vregisters)
				else
					puts "FOUND GETSYSTEMSERVICE without map"
				end
			end
			
		when /^invoke-.*\{(.*)\},(\S+)\s*;\s*\S+(\(.*\))Ljava\/lang\/String;/
			methodname="#{$2}#{$3}"
			params = get_param_regs($1)
			if $method_names.include?(methodname) && first<2
				if not line =~ /^invoke-static/
					params = params[1..-1]
				end
				array = make_param_array(params, vregisters)
				returnvalue = look_for_values(methodname, $code[methodname], first+1, array, "#{path},#{methodname}")
				return_reg = find_return_register(code, i)
				recordRegister(return_reg, "string", returnvalue, vregisters)
				puts "string: #{returnvalue}, #{return_reg}"
			elsif $method_returns_str.has_key?(methodname)
				return_reg = find_return_register(code, i)
				value=""
				if $method_returns_str[methodname] == ""
					value = "**unknown"
				else
					value = $method_returns_str[methodname]
				end
				puts "string: #{value}, #{return_reg}"
				recordRegister(return_reg, "string", value, vregisters)
			end
		when /^invoke-.*\{(.*)\},(\S+)\s*;\s*\S+(\(.*\))Ljava\/lang\/reflect\/Method;/
			methodname="#{$2}#{$3}"
			params = get_param_regs($1)
			if $method_names.include?(methodname) && first<2
				if not line =~ /^invoke-static/
					params = params[1..-1]
				end
				array = make_param_array(params, vregisters)
				returnvalue = look_for_values(methodname, $code[methodname], first+1, array, "#{path},#{methodname}")
				return_reg = find_return_register(code, i)
				recordRegister(return_reg, "method", returnvalue, vregisters)
				puts "returned from method: #{returnvalue}, #{return_reg}"
			elsif $method_returns_meth.has_key?(methodname)
				return_reg = find_return_register(code, i)
				value=""
				if $method_returns_meth[methodname] == ""
					value = "**unknown"
				else
					value = $method_returns_meth[methodname]
				end
				puts "method: #{value}, #{return_reg}"
				recordRegister(return_reg, "method", value, vregisters)
			end
		when /^invoke-.*\{(.*)\},(\S+)\s*;\s*\S+(\(.*\))Ljava\/lang\/reflect\/Constructor;/
			methodname="#{$2}#{$3}"
			params = get_param_regs($1)
			if $method_names.include?(methodname) && first<2
				if not line =~ /^invoke-static/
					params = params[1..-1]
				end
				array = make_param_array(params, vregisters)
				returnvalue = look_for_values(methodname, $code[methodname], first+1, array, "#{path},#{methodname}")
				return_reg = find_return_register(code, i)
				recordRegister(return_reg, "constructor", returnvalue, vregisters)
				puts "constructor: #{returnvalue}, #{return_reg}"
			elsif $method_returns_cons.has_key?(methodname)
				return_reg = find_return_register(code, i)
				value=""
				if $method_returns_cons[methodname] == ""
					value = "**unknown"
				else
					value = $method_returns_cons[methodname]
				end
				puts "constructor: #{value}, #{return_reg}"
				recordRegister(return_reg, "constructor", value, vregisters)
			end
			
		when /^invoke-.*\{(.*)\},(\S+)\s*;\s*\S+(\(.*\))Ljava\/lang\/Class;/
			#puts "Found method that returns class"
			methodname="#{$2}#{$3}"
			params = get_param_regs($1)
			#puts "Method: #{methodname}"
			if $method_names.include?(methodname) && first<2
				#puts "Found method that returns class2"
				if not line =~ /^invoke-static/
					params = params[1..-1]
				end
				array = make_param_array(params, vregisters)
				returnvalue = look_for_values(methodname, $code[methodname], first+1, array,"#{path},#{methodname}")
				return_reg = find_return_register(code, i)
				recordRegister(return_reg, "class", returnvalue, vregisters)
				puts "class: #{returnvalue}, #{return_reg}"
			elsif $method_returns_cls.has_key?(methodname)
				return_reg = find_return_register(code, i)
				value=""
				if $method_returns_cls[methodname] == ""
					value = "**unknown"
				else
					value = $method_returns_cls[methodname]
				end
				puts "class: #{value}, #{return_reg}"
				recordRegister(return_reg, "class", value, vregisters)
			end
			
		#handles returned Object calls AND also when getSystemService is this.getSystemService
		when /^invoke-.*\{(.*)\},(\S+)\s*;\s*\S+(\(.*\))Ljava\/lang\/Object;/
			methodname="#{$2}#{$3}"
			params = get_param_regs($1)
			if !$method_names.include?(methodname) && methodname.include?("getSystemService")
			  reg = get_register(line, 1)
  			if correctRegisterType(reg, "string", vregisters)
  				if $stringToClass.has_key?(vregisters[reg].value)
  					return_reg = find_return_register(code, i)
            puts "object: systemService #{vregisters[reg].value} -> #{$stringToClass[vregisters[reg].value]}, #{return_reg}"
  					recordRegister(return_reg, "object", $stringToClass[vregisters[reg].value], vregisters)
  				else
  					puts "FOUND GETSYSTEMSERVICE without map"
  				end
  			end
  		#otherwise it's a recursive call
			elsif $method_names.include?(methodname) && first<2
				#puts "Found method that returns object"
				if not line =~ /^invoke-static/
					params = params[1..-1]
				end
				array = make_param_array(params, vregisters)
				returnvalue = look_for_values(methodname, $code[methodname], first+1, array, "#{path},#{methodname}")
				return_reg = find_return_register(code, i)
				recordRegister(return_reg, "object", returnvalue, vregisters)
				puts "object: #{returnvalue}, #{return_reg}"
			elsif $method_returns_obj.has_key?(methodname)
				return_reg = find_return_register(code, i)
				puts return_reg
				value=""
				if $method_returns_obj[methodname] == ""
					value = "**unknown"
				else
					value = $method_returns_obj[methodname]
				end
				puts "object: #{value}, #{return_reg}"
				recordRegister(return_reg, "object", value, vregisters)
			end		

		when /return-object\s+(v\d+)/
			puts "Found RETURN call #{first.to_s}"
			reg =$1
			
			if correctRegisterType(reg, "num", vregisters) && vregisters[reg].value == "0"
			  puts "Ran into a return call, but continuing on"
			  next
			end
			
			record_method_return_result(method, vregisters, reg)
			
			if first!=0
				if hasRegister(reg, vregisters)
					puts "Returning #{vregisters[reg].value} #{method}"
					return vregisters[reg].value
				else
					puts "Returning **unknown"
					return "**unknown"
				end
			else
			  puts "Encountered first depth return, but continuing on"
			end

		when /goto\s+(\S+)/
		  jumplocation = $1
			nearend = is_near_end_method(code, i)
			if nearend
			  puts "Found goto near end.  Jumping to label"
			  jmpIndex = code.index("#{jumplocation}:")
			  possibleregister = is_near_returnobj(code, jmpIndex)
			  if possibleregister != "0"
          record_method_return_result(method, vregisters, possibleregister)
        end
        if first!=0
				  if hasRegister(possibleregister, vregisters)
					  puts "Returning #{vregisters[possibleregister].value} #{method}"
		  		  return vregisters[possibleregister].value
				  else
					  puts "Returning **unknown"
					  return "**unknown"
				  end
			  end
			end
			
		when /^\.end method/
			if first!=0
				puts "End of method: #{method}"
				return "**unknown"
			end

		end
	end
end

def combinePackageAndMethod(methodName, methodPackage)
  temp="**unknownClass.**unknownMethod"
  if !methodName.include?(".") && !methodName.include?("/")
    parts = methodPackage.split("/").join(".").split(".")
    if parts.size>1
      temp = "#{parts[0..-2].join(".")}.#{methodName}"
    else
      temp = "**unknownClass.#{methodName}"
    end
  else
    temp = "**unknownClass.#{methodName}"
  end
  return temp
end


def getName(value)
  vals = value.split("/").join(".").split(".")
  return vals[-1]
end

def record_method_return_result(method, vregisters, reg)
	if $method_returns_str.has_key?(method) && correctRegisterType(reg, "string", vregisters)
		$method_returns_str[method] = vregisters[reg].value
		puts "Recording string #{vregisters[reg].value} #{method}"
	elsif $method_returns_cls.has_key?(method) && correctRegisterType(reg, "class", vregisters)
		$method_returns_cls[method] = vregisters[reg].value
		puts "Recording class #{vregisters[reg].value} #{method}"
	elsif $method_returns_meth.has_key?(method) && correctRegisterType(reg, "method", vregisters)
		$method_returns_meth[method] = vregisters[reg].value
		puts "Recording method #{vregisters[reg].value} #{method}"
	elsif $method_returns_cons.has_key?(method) && correctRegisterType(reg, "constructor", vregisters)
		$method_returns_cons[method] = vregisters[reg].value
		puts "Recording constructor #{vregisters[reg].value} #{method}"
	elsif $method_returns_obj.has_key?(method) && hasRegister(reg, vregisters)
		$method_returns_obj[method] = vregisters[reg].value
		puts "Recording object #{vregisters[reg].value} #{method}"
	end
end

def set_called_dests(reflect, path, value)
  if reflect.calledDests.has_key?(path)
    return reflect.calledDests[path].push(value).uniq
  else
    return [value]
  end
end

def make_param_array(params, vregisters)
	array = []
	params.each do |p|
		if hasRegister(p, vregisters)
			array.push(vregisters[p].value)
		else
			array.push("**unknown")
		end
	end
	return array
end


def get_comment_type(line, reg)
	regs = line.split(',')
	regs.each do |r|
		if r=~/#{reg}\s+:\s+(.*);/
			return $1
		end
	end
end

def is_near_end_method(code, i)
	code[i+1..i+3].each do |x|
		if x=~ /^.end method/
			return true
		end
	end
	return false
end

def is_near_returnobj(code, i)
	code[i+1..i+3].each do |x|
		if x=~ /^return-object\s+(v\d+)/
			return $1
		end
	end
	return "0"
end

def find_return_register(code, i)
	code[i+1..i+4].each do |x|
		if x=~ /^move-result-object\s+(v\d+)/
			return $1
		end
	end
	return "-1"
end

def recordRegister(name, type, value, vregisters)
	reg= Register.new(name, type, value)
	vregisters[name]=reg
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

def loadContentMap(file, map)
	f = File.new(file)
	begin
		while (line = f.readline)
			line.chomp!
			parseStr = line.split(' ')
			if parseStr.size ==2
				map[parseStr[1]] = parseStr[0]    #Note: swapping the order
			else
				puts "Bad format in #{file} list"
			end 
		end
	rescue EOFError
		f.close
	end
end

def findReverseCallGraph()
  $callGraph.keys.each do |key|
    calls = $callGraph[key]
    calls.each do |call|
      if $method_names.include?(call)
        if $reverseCallGraph.has_key?(call)
          $reverseCallGraph[call] = $reverseCallGraph[call].push(key)
        else
          $reverseCallGraph[call] = [key]
          #puts "Found method"
        end
      else
        #puts "Debugging: not adding #{call}"  
      end
    end
  end
  
  $reverseCallGraph.keys.each do |key|
    $reverseCallGraph[key] = $reverseCallGraph[key].uniq
  end
end

def isReflectionResolutionUnsucessful(dest)
  if dest == ""
    return true
  elsif dest == "0"
      return true
  elsif ((dest =~ /0\//) || (dest =~ /0./) || (dest =~ /.0/) || (dest =~ /\/0/))
      return true
  elsif dest =~ /\*\*unknown/
    return true
  elsif ((dest =~ /java.lang.Object/) || (dest =~ /java\/lang\/Object/))
		return true
	else
	  return false
	end
end

def doesMethodTakeStringMethConsObjParam(meth)
  if meth =~/.*\((.*)\)/
    params =$1
    if meth =~/Ljava\/lang\/Object/
      return true
    elsif meth =~/Ljava\/lang\/String/
      return true
    elsif meth =~/Ljava\/lang\/reflect\/Method/
      return true
    elsif meth =~/Ljava\/lang\/reflect\/Constructor/
      return true
    elsif meth =~/Ljava\/lang\/Class/
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
  
  $reflect_names.each do |name|
		if isReflectionResolutionUnsucessful($reflection[name].dest)
		  call = $reflection[name].inMethod
		  $secondPassReflections.push(name)
		  if doesMethodTakeStringMethConsObjParam(call) && $reverseCallGraph.has_key?(call)
		    $reverseCallGraph[call].delete_if {|x| x == call }
		    callingMethods = callingMethods + $reverseCallGraph[call]
		  end
		end
	end
  
  callingMethods = callingMethods.uniq
  callingMethods2=[]
  callingMethods.each do |call|
    if doesMethodTakeStringMethConsObjParam(call) && $reverseCallGraph.has_key?(call)
      $reverseCallGraph[call].delete_if {|x| x == call }
      callingMethods2 = callingMethods2 + $reverseCallGraph[call]
    end
  end
    
  return (callingMethods+callingMethods2).uniq
end

def formatCall(dest)
  call="#{dest.split("/").join(".")}"
  if call.start_with?('L')
    call=call[1..-1]
  end
  return call
end

def main()
	#puts "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
	get_cmd_args
	folder = ARGV[0]
	$outputdir= ARGV[1] # "../ReflectionResults/#{$folder}/#{$appname}/"
	$appname = ARGV[2]
	puts $appname
	ddxfilelist = "#{folder}DDXFILELIST"
	
	banner("Finding use of newInstance and invoke in #{$appname} DDX ...")
	get_file_list(ddxfilelist).each() do |filename|
		record_methods(filename)

		$class_name  = ""
		$class_super = ""
		$source_file = ""
	end
	
  if $reflect_names.length>0								#only search if reflection was used
	
		loadContentMap("classToService.txt", $classToService)
		loadContentMap("classToInterface.txt", $classToInterface)
		
		banner("Finding method call...")
		
    findReverseCallGraph()
    
    #inits, clinits, returns str, returns cls, returns cons, returns method, returns obj, forName, getDeclaredMethod/Cons
		methodstocheck = $investigate_methods1
		methodstocheck = methodstocheck.concat($investigate_methods3)
		methodstocheck = methodstocheck.concat($method_returns_str.keys)
		methodstocheck = methodstocheck.concat($method_returns_cls.keys)
		methodstocheck = methodstocheck.concat($method_returns_cons.keys)
		methodstocheck = methodstocheck.concat($method_returns_meth.keys)
		methodstocheck = methodstocheck.concat($method_returns_obj.keys)
		methodstocheck = methodstocheck.concat(($investigate_methods+$investigate_methods2).uniq)

		reflectfuncs=[]
		$reflect_names.uniq.each do |i|
			reflectfuncs.push($reflection[i].inMethod)
		end
		methodstocheck = methodstocheck.concat(reflectfuncs.uniq)
		
		methodstocheck.each do |method|
			puts method if $options[:verbose]
			code = $code[method]
			banner("Processing #{method}...")
			look_for_values(method, code, 0, [], "#{method}")
			puts "***" if $options[:verbose]
		end
		
		banner("Second pass processing...")
    callingMethods = getExtraCallingMethods()
    (callingMethods-methodstocheck).each do |method|
			puts method if $options[:verbose]
			code = $code[method]
			banner("Processing #{method}...")
			look_for_values(method, code, 0, [], "#{method}")
			puts "***" if $options[:verbose]
		end

  	banner("Analysis order...")
    methodstocheck.each do |method|
      puts method
  	end
  	banner("Analysis order for 2nd Pass...")
  	callingMethods.each do |method|
      puts method
  	end    
		
	end
	
	banner("Find method...")
	print_reflections()

	debug=[]
	$reflect_names.each do |name|

    symbol = ""
	  debug.push("For sink at: #{name}")
	  if !isReflectionResolutionUnsucessful($reflection[name].dest) || $reflection[name].calledDests.keys.length == 0 #or not doesMethodTakeStringMethConsObjParam($reflection[name].inMethod) #not $secondPassReflections.include?(name) 
	    symbol = "*"
	  end
	  
	  debug.push("  orig:")
	  dest = $reflection[name].dest
	  if !$reflection[name].done
		  debug.push("#{symbol}    not done: #{name}")
	  elsif dest.include?("java\/lang\/Object\/") || dest.include?("java.lang.Object.")
		  debug.push("#{symbol}    object: #{dest}")
	  elsif dest.include?("**unknown")
		  debug.push("#{symbol}    unknown: #{dest}")
		elsif ((dest == "0") || (dest =~ /0\//) || (dest =~ /0./) || (dest =~ /.0/) || (dest =~ /\/0/))
		  debug.push("#{symbol}    failure: #{dest}")
		else
		  debug.push("#{symbol}    successful: #{dest}")
	  end
	  
	  if symbol == "" #and doesMethodTakeStringMethConsObjParam($reflection[name].inMethod)
	    symbol = "*"
	  else
	    symbol = ""
	  end
	  
    debug.push("  callers:")	  
    $reflection[name].calledDests.keys.each do |path|
      dests = $reflection[name].calledDests[path]
      dests.each do |dest|
	      if !$reflection[name].done
		      debug.push("#{symbol}    not done: #{name}, [at #{path}]")
	      elsif dest.include?("java\/lang\/Object\/") || dest.include?("java.lang.Object.")
		      debug.push("#{symbol}    object: #{dest}, [at #{path}]")
	      elsif dest.include?("**unknown")
		      debug.push("#{symbol}    unknown: #{dest}, [at #{path}]")
    		elsif ((dest == "0") || (dest =~ /0\//) || (dest =~ /0./) || (dest =~ /.0/) || (dest =~ /\/0/))
    		  debug.push("#{symbol}    failure: #{dest}, [at #{path}]")
	      else
  		    debug.push("#{symbol}    successful: #{dest}, [at #{path}]")
	      end
	    end
		end
	end
	
	File.open("#{$outputdir}reflectiveDebug.txt", 'w+') do |f|
		debug.each do |name|
			f.write("#{name} \n")
		end
	end 
	
	debugfailures=[]
	unknown=" **unknown"
	$reflect_names.each do |name|
	  if !$reflection[name].found
	    failures = "#{name}"
	    if isReflectionResolutionUnsucessful($reflection[name].dest)
	      if $reflection[name].dest == ""
	         failures = failures + unknown
	      else
	        call=formatCall($reflection[name].dest)
	        failures = failures + " #{call}"
	      end
	      $reflection[name].calledDests.keys.each do |path|
  		    dests = $reflection[name].calledDests[path]
          dests.each do |dest|
            if isReflectionResolutionUnsucessful(dest)
              if $reflection[name].dest == ""
      	         failures = failures + unknown
       	      else    	      
       	        call=formatCall($reflection[name].dest)
      	        failures = failures + " #{call}"
      	      end
  		      end
  		    end
  		  end
  		end
  		debugfailures.push(failures)
	  end
	end
	
	File.open("#{$outputdir}reflectiveDebugSinkFailures.txt", 'w+') do |f|
		debugfailures.each do |name|
			f.write("#{name}\n")
		end
	end

	forNameformat=[]
	$forNameUse.each do |name|
		call=formatCall(name)
		forNameformat.push(call)
	end
	
	File.open("#{$outputdir}forNameUse.txt", 'w+') do |f|
		forNameformat.uniq.sort.each do |name|
			f.write("#{name}\n")
		end
	end

	File.open("#{$outputdir}MethodOrConsUse.txt", 'w+') do |f|
		$methodcons_names.each do |name|
		  $methodcons[name].dest.each do |dest|
			  call=formatCall(dest)
			  f.write("#{call}\n")
			end
		end
	end

	finalformat=[]
	$reflect_names.each do |name|
		if $reflection[name].done
      dest=$reflection[name].dest
		  call=formatCall(dest)
		  finalformat.push(call)
		  #if isReflectionResolutionUnsucessful($reflection[name].dest) #$secondPassReflections.include?(name)
		    $reflection[name].calledDests.keys.each do |path|
          dests = $reflection[name].calledDests[path]
          dests.each do |dest|
			      call=formatCall(dest)
			      finalformat.push(call)
			    end
			  end
		  #end
		end
	end

  finalformat=finalformat.uniq.sort        
  File.open("#{$outputdir}reflectivecalls.txt", 'w+') do |f|
		finalformat.each do |name|
			f.write("#{name}\n")
		end
	end 

end

main()
