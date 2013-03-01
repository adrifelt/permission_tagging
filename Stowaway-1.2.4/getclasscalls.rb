#!/usr/bin/ruby

$class_name  = ""
$class_super = ""
$source_file = ""
$method_name = ""
$entry_vertex = "ENTRY"
$main_entry = "MAIN_ENTRY"
$line = nil
$last_line = nil
$line_num = ""
$all_lines = []
$intent_destination = ""
$declared_methods = []
$called_methods = []
$soup = {}
$getnext = false

def strip_method_name_args(method)
		path ='' 
		if ($method_name.split(' ').size == 1 ) then
			path += method
		else
			sr = $method_name.split(' ')
			path += sr[sr.size - 1] # add method name
		end
		argument_start = path.index("(")
		path = path[0..argument_start - 1]
end

def strip_classpath(method)
	split_result = method.split('/')	
	if (split_result.size == 0) then
		return method	
	end
	return split_result[split_result.size - 1]
end

def canonicalize_method_name(method)
		path = ""
		if ($class_name.split(' ').size == 0 ) then
		   path = ""
		elsif ($class_name.split(' ').size == 1 ) then
			path = $class_name	
		else
			sr = $class_name.split(' ')
			path = path + sr[sr.size - 1] 
		end

		path += "/"
		path += strip_method_name_args(method)
		path
end

def finish_function()
		$method_name = canonicalize_method_name($method_name)
		$declared_methods.push($method_name)
		$method_name = ""
end

def handle_line(line, directive, data)
	case directive
	when "class"
	    $split = data.split
			$class_name = $split[$split.length-1]
	when "super"
			$class_super = data
			$soup[$class_name] = $class_super
	when "source"
			$source_file = data
	when "field"
			#nothing
	when "method"
			$method_name = data
	when "limit"
			#nothing
	when "line"
			$line_num = data
	when "end"
			if data.strip == "method" then
					finish_function()
			end
	end
end

def handle_instruction(line, directive, data)
	function_name = clean_invokation(line)

	case directive
	when "virtual"
	    if (function_name =~ /.*getClass$/) then
  			  $getnext = true
			end
	end	
	return 0
end

#Returns canonicalized function name
def clean_invokation(line)
	semi_split = line.split(';')
	comment = semi_split[1].strip
	fn_split = semi_split[0].split(',')
	function_name = fn_split[fn_split.size() - 1].strip
	return function_name
end

def handle_comment(line)
end

def parse_line(line)
	if (/\S/ !~ line) then 
		return #blank line
	end
	if ($getnext) then
	  if (line.strip =~ /.* : L(.*);/) then
        $called_methods.push($1)
        return
    end
    $getnext=false
	end
	if (line.strip =~ /^\.(interface) (.*)/) then
	  return 10
	elsif (line.strip =~ /^\.(class|super|source|field|method|limit|line|end) (.*)/) then
	  handle_line(line, $1, $2)
	elsif (line.strip =~ /^;/) then
		handle_comment(line)
	elsif(line.strip =~ /^invoke-(virtual|direct|super|static|interface)(.*?)/) then
		handle_instruction(line, $1, $2)	
	end

end

def read_file(fn)
		f = File.new(fn)
		begin
				while ($line = f.readline)
				if ( parse_line($line) == 10 ) 
				  break
				end					
				$last_line = $line
				$all_lines.push($line)
				end
		rescue EOFError
				f.close
		end
		
		#Reset all lines parsed for each file
		$all_lines = []
end


def get_file_list(fn)
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

def print_found_methods_api()
    for method in $called_methods do
			  print method + "\n"
		end
end

def main()
		ARGV.each() do |filelist| 
				get_file_list(filelist).each() do |filename| 
						$printed_banner = false
						read_file(filename)
				end
		end		
		print_found_methods_api()
end
main()
