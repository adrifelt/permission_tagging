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
output="../ReflectionResults/stats/allreflectivecalls.txt"

allcalls=[]
apps=get_file_list(filelist)

apps.each() do |filename|
	puts filename
	calls=get_file_list("../ReflectionResults/#{filename}/reflectivecalls.txt")
	allcalls.concat(calls.uniq)
end

allcalls = allcalls.uniq.sort
File.open(output, 'w') do |f|
	allcalls.each do |call|
		f.write("#{call}\n")
	end
end
