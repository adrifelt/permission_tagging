#
#  Register.rb
#  
#
#  Created by Erika Chin on 11/1/10.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

class Register
    attr_accessor :name, :objType, :value, :linkedTo, :isOrigConst, :from

def initialize(nam, oType, val)
	@name=nam
	@objType=oType
	@value=val
	@linkedTo = []
    @isOrigConst = false
    @from=""
end

def setRegister(nam, oType, val)
	@name=nam
	@objType=oType
	@value=val
end

def getType()
	return @objType
end

def addLink(reg)
	if reg != @name
		@linkedTo.push(reg)
		@linkedTo = @linkedTo.uniq
	end
end

def removeLink(reg)
	if @linkedTo.include?(reg)
		@linkedTo.delete(reg)
	end
end

def copyLinks(register)
	@linkedTo=Marshal.load( Marshal.dump(register.linkedTo))
	@linkedTo = @linkedTo.uniq
	if @linkedTo.include?(@name)
		@linkedTo.delete(@name)
	end
end
end
