#
#  ReflectObj.rb
#  
#
#  Created by Erika Chin on 10/26/10.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

class ReflectObj

    attr_accessor :name, :line, :line_num, :inMethod, :type, :done, :found, :dest, :classUnknown, :calledDests
def initialize(meth, lnum, line, type)
	@name=meth+"@"+lnum.to_s	#name
	@line=line				#invocation
	@line_num=lnum			#line num in ddx
	@inMethod=meth			#method it appears in 
	@type=type				#method call or constructor init
	@done=false				#if the parser finds this call with valid register
	@found=false			#if it finds the method/constructor called
	@dest = ""
    @calledDests = {}
	@classUnknown=false
end

end
