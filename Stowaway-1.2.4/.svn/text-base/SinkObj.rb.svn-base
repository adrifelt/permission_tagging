#
#  SinkObj.rb
#  
#
#  Created by Erika Chin on 10/26/10.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

class SinkObj

attr_accessor :name, :line, :line_num, :source_line_num, :inMethod, :type, :done, :intents, :compType, :permission

def initialize(meth, lnum, slnum, line, type, ctype)
	@name=meth+"@"+lnum.to_s	#name
	@line=line				#invocation
	@line_num=lnum			#line num in ddx
	@source_line_num=slnum  #line num in source
	@inMethod=meth			#method it appears in 
	@type=type				#method call name
	@compType=ctype			#component dest type
	@done=false				#if an intent had been found that goes to it
	@intents = []			#all intents that go to it
	@permission = ""
end

def addIntent(intent)
	@intents.push(intent)
end
end
