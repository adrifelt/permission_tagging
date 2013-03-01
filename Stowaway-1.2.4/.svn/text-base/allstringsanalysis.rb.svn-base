#!/usr/bin/ruby

require 'optparse'


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

$all_strings=[]

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

def parse_for_method(line)
	line = line.strip
	if (/\S/ !~ line) then 
		return
	end
	
	if ($in_method == true) then
		$method_code.push(line.strip)
		$line_count= $line_count+1
	end
	if (line.strip =~ /^\.(class|super|source|field|method|limit|line|end|inner|implements|annotation|interface) (.*)/) then
		handle_line(line.strip, $1, $2)
	elsif(line.strip =~ /^const-(string)\s+(v[0-9]+),\"(.*)\"/)
		$all_strings.push($3)
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
					#puts value
					$all_strings.push(value)
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




def main()
	#puts "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
	get_cmd_args
	folder = ARGV[0]
	$outputdir= ARGV[1]
	$appname = ARGV[2]
	#puts $appname
	ddxfilelist = "#{folder}DDXFILELIST"
	
	#banner("Parsing DDX")
	get_file_list(ddxfilelist).each() do |filename|
		record_methods(filename)
		#$methods_for_class[slash_to_dot($class_name)]=$methods_in_class
		#$methods_in_class=[]
		$class_name  = ""
		$class_super = ""
		$source_file = ""
	end

	File.open("#{$outputdir}allStrings.txt", 'w+') do |f|
		$all_strings.uniq.each do |name|
			f.write("#{name}\n")
		end
	end 
end

main()
