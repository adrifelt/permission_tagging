#!/usr/bin/ruby

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

filelist="../ReflectionResults/filelist"
output="../ReflectionResults/stats/totalcountlist"
output2="../ReflectionResults/stats/probcountlist"
$count= {}
File.open(output, 'w') {|f| f.write("Name \t\t\t\t\t\t\tNum found Num Done Num obj Total\n") }
File.open(output2, 'w') {|f| f.write("Name \t\t\t\t\t\t\tNum found Num Done Num obj Total\n") }
get_file_list(filelist).each() do |filename|
	$count= {}
	puts filename
	File.open("../ReflectionResults/#{filename}/count") do |f|  
		$count=Marshal.load(f)
	end
	appname=filename.split('/')[1]
	if appname.size<55
		spaces=55-appname.size
		spaces.times{|i| appname=appname.concat(' ')}
	end
	type=["numfound", "numdone", "objfound", "total"]

	File.open(output, 'a') {|f| f.write("#{appname}\t\t#{$count['numfound']}\t#{$count['numdone']}\t#{$count['objfound']}\t#{$count['total']} \n") }

	if $count['total'] != 0 and ($count['total'] != $count['numfound'])
		File.open(output2, 'a') {|f| f.write("#{appname}\t\t#{$count['numfound']}\t#{$count['numdone']}\t#{$count['objfound']}\t#{$count['total']} \n") }
	end
end
