#
#  IntentObj.rb
#  
#
#  Created by Erika Chin on 10/26/10.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

class IntentObj
attr_accessor :name, :line, :line_num, :source_line_num, :method, :isMethodParam, :type, :registers, :init_line_num, :explicit, :explicit_destination, :dest_type, :done, :limitation, :sink_line, :is_init, :returned, :hasExtra, :hasChooser, :hasURI, :hasFlagRead, :hasFlagWrite, :action
	#@name=""				#name of method+@+line_num		#@line=""				#Dalvik code line
	#@line_num=0			#line num (counted from beginning of method)
	#@source_line_num=0		#line num from source code
	#@method=""				#name of method where it appears

	#@isMethodParam=false	#is it a method declaration?

	#@type=0				#type of constructor
	#@registers=[]			#registers holding intent
	#@init_line_num=0		#line num of the init
	
	#@explicit=false		#explicit or implicit intent
	#@explicit_destination=""	#component destination
	#@dest_type=""			#broadcast, service, activity
	#@done=false			#whether it has been processed
	#@limitation=""			#package limitation
	
def initialize(meth, lnum, line, src_lnum)
	@name=meth+"@"+lnum.to_s
	@line=line
	@line_num=lnum
	@source_line_num=src_lnum
	@method=meth

	@isMethodParam=false

	@type=0
	@registers=[]
	@init_line_num=0
	@is_init=false
	
	@explicit=false
	@explicit_destination=""
	@dest_type=""
	@sink_line=""
	@done=false
	@limitation=""
	
	@returned=false
	
	@hasExtra=false
	@hasChooser=false
	@hasURI=false
	@hasFlagRead=false
	@hasFlagWrite=false
	
	@action=[]

end

def addregister(reg)
	if hasregister(reg) == false then
		@registers.push(reg)
		puts "Adding register #{reg}" if $options[:debug] 

	end
end
def removeregister(reg)
	if hasregister(reg) == true then
		@registers.delete(reg)
		puts "Removing register #{reg}" if $options[:debug] 
	end
end
def hasregister(reg)
	return @registers.include?(reg)
end

end
