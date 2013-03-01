#!/usr/bin/ruby

require 'optparse'
require 'Register'

$appname= ""
$outputdir=""

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

$uri_list =[]
$investigate_methods=[]
$vregisters={}

$uriToContent={}

$MAYCHANGE = " mayChange"
$NOCHANGE = " noChange"
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

def format_URI(str)
	str = str.split('/').join('.')
	str = str.split('$').join('.')
	return str
end

def convertUri(str)
	if $uriToContent.has_key?(str)
		return $uriToContent[str]
	else
		if str.start_with?("android.")
			puts "Could not return content for #{str}"
		else
			puts "Non-android uri #{str} not added"
		end
		return "ERROR"
	end
end

def parse_for_method(line)
	line = line.strip
	if (/\S/ !~ line) then 
		return
	end
	
	if ($in_method == true) then
		$method_code.push(line.strip)
		$line_count= $line_count+1
	end
	if (line =~ /\.(INTERNAL_CONTENT_URI|EXTERNAL_CONTENT_URI|CONTENT_FILTER_URI|CONTENT_URI|BOOKMARKS_URI|SEARCHES_URI|CONTENT_URI)/) then
		if (line=~/^(s..t|i..t)-object\s+(v[0-9]+,)+(.*(\.INTERNAL_CONTENT_URI|\.EXTERNAL_CONTENT_URI|\.CONTENT_FILTER_URI|\.CONTENT_URI|\.BOOKMARKS_URI|\.SEARCHES_URI)).*\s+Landroid\/net\/Uri;/)
			str = format_URI($3)
			value = convertUri(str)
			if value != "ERROR"
				#puts "Found #{value}"
				$uri_list.push(value+$NOCHANGE)
			end
		elsif(line=~/^const-string\s+(v[0-9]+,)+\"(.*\.CONTENT_URI)\"/)
			str = format_URI($2)
			value = convertUri(str)
			if value != "ERROR"
				puts "***Const #{str}"
				#puts "Found #{value}"
				$uri_list.push(value+$NOCHANGE)
			end
		else
			puts "***Could not parse #{line}"
			#$uri_list.push(value+$NOCHANGE)

		end
	elsif(line =~ /^const-(string)\s+(v[0-9]+),\"(.*)\"/)
		str = $3
		if str=~/^content:\/\//
			if str == "content://"
				puts "***Only content://"
			else
				$uri_list.push(str+$MAYCHANGE)
			end
		end
	elsif(line =~ /^invoke-static\s+\{.*\},android\/net\/Uri\/fromParts/)
		$investigate_methods.push($method_name)
	end
	if (line =~ /^\.(class|super|source|field|method|limit|line|end|inner|implements|annotation|interface) (.*)/) then
		handle_line(line, $1, $2)
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
			if type == "Ljava/lang/String"
				if parsed.size>1 and parsed[1].include?("\"")
					value = parsed[1].strip.delete('\"')
					if value=~/^content:\/\//
						#puts "***Field: #{value}"
						if value == "content://"
							puts "***Field, only Content: #{value}"
						else
							$uri_list.push(value+$MAYCHANGE)
						end
					end
				end
			end
	when "method"
			$line_count = 0
			$in_method = true
			$method_code.push(line.strip)
			$method_name = canonicalize_method_name(data)
			$method_names.push($method_name)

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

def look_for_values(method, code)
	$vregisters={}
	$line_num=-1
	code.each_with_index.each() do |line, i|
		case line
		when /^.line\s+(\d+)/
			$line_num = $1
		when /^;\s+parameter\[\d+\]\s+:\s+(v\d+)\s+\(Ljava\/lang\/String;\)/
			recordRegister($1, "string", "**unknownStringParam")
			puts "string: unknownStringParam, #{$1}"  if $options[:debug]
		when /^const-(string)\s+(v[0-9]+),\"(.*)\"/
			recordRegister($2, $1, $3)
			puts "string: #{$3}, #{$2}"  if $options[:debug]
		when /^const-\S+\s+(v[0-9]+),.*/
			removeRegister($1)
		#when /^new-instance\s+(v[0-9]+),/
		#	removeRegister($1)
		when /^move-object.*(v[0-9]+),(v[0-9]+)/
			reg1=$1
			reg2=$2
			if $vregisters.has_key?(reg2)
				recordRegister(reg1, $vregisters[reg2].getType, $vregisters[reg2].value)
				$vregisters[reg1].copyLinks($vregisters[reg2])
				$vregisters[reg2].addLink(reg1)
				$vregisters[reg1].addLink(reg2)
				puts "Update Reg: #{$vregisters[reg1].name} #{$vregisters[reg1].getType} #{$vregisters[reg1].value}" if $options[:debug]
			elsif $vregisters.has_key?(reg1) and not $vregisters.has_key?(reg2) 
				puts "Deleting Reg: #{$vregisters[reg1].name}"  if $options[:debug]
				$vregisters.delete(reg1)
			end
		when /^invoke-static\s+\{.*\},android\/net\/Uri\/fromParts/
			puts "***fromParts found" if $options[:debug]
			reg1 = get_register(line, 0)
			reg2 = get_register(line, 1)
			reg3 = get_register(line, 2)
			val1 = "**unknown"
			val2 = "**unknown"
			val3 = "**unknown"
			if correctRegisterType(reg1, "string")
				val1=$vregisters[reg1].value
			end
			if correctRegisterType(reg2, "string")
				val2=$vregisters[reg2].value
			end
			if correctRegisterType(reg3, "string")
				val3=$vregisters[reg3].value
			end
			if (val1 == "content")
				#puts "***#{val1}://#{val2}"
				$uri_list.push("#{val1}://#{val2}#{$NOCHANGE}")
			elsif (val1 == "**unknown")
				puts "***fromParts: Unknown scheme; not added to output"
			end
		end
	end
end

def get_comment_type(line, reg)
	regs = line.split(',')
	regs.each do |r|
		if r=~/#{reg}\s+:\s+(.*);/
			return $1
		end
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

def recordRegister(name, type, value)
	reg= Register.new(name, type, value)
	$vregisters[name]=reg
end

def hasRegister(name)
	if $vregisters.has_key?(name)
		return true
	else
		return false
	end
end

def correctRegisterType(name, type)
	if hasRegister(name) and $vregisters[name].getType == type
		return true
	else
		return false
	end
end

def removeRegister(reg)
	if hasRegister(reg)
		$vregisters.delete($1)
		$vregisters.keys.each do |i|
			if i != reg
				$vregisters[i].removeLink(reg)
			end
		end
	end
end

def loadUriToContentMap(file)
	f = File.new(file)
	begin
		while (line = f.readline)
			line.chomp!
			parseStr = line.split(' ')
			if parseStr.size ==2
				$uriToContent[parseStr[0]] = parseStr[1]
			else
				puts "Bad format in #{file} list"
			end 
		end
	rescue EOFError
		f.close
	end
end


def main()

	get_cmd_args
	folder = ARGV[0]
	$outputdir= ARGV[1]
	$appname = ARGV[2]
	#puts $appname
	ddxfilelist = "#{folder}DDXFILELIST"
	
	loadUriToContentMap("androidProviderList.txt")
	
	#banner("Parsing DDX")
	get_file_list(ddxfilelist).each() do |filename|
		record_methods(filename)
		$class_name  = ""
		$class_super = ""
		$source_file = ""
	end

	$investigate_methods.each do |method|
		code = $code[method]
		look_for_values(method, code)
	end


	File.open("#{$outputdir}URIuse.txt", 'w+') do |f|
		$uri_list.uniq.sort.each do |name|
			f.write("#{name}\n")
		end
	end 

end

main()
