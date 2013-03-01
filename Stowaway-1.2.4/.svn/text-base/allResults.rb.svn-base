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
output="../ReflectionResults/stats/allreflectivecallswfilename.txt"

allcalls=[]
apps=get_file_list(filelist)

apps.each() do |filename|
	calls=get_file_list("../ReflectionResults/#{filename}/reflectivecalls.txt")

	File.open(output, 'a') do |f|
		if calls.size != 0
			f.write("\n#{filename}\n")
		end
		calls.each do |call|
			f.write("#{call}\n")
		end
	end
end
