#!/usr/bin/ruby

require "rexml/document"
include REXML

file = File.new(ARGV[0])
doc = REXML::Document.new file

$packageName = doc.root.attributes["package"]
if $packageName.nil?
	$stderr.puts("***Package Name is nil***")
	exit
end

permissions = doc.elements.to_a("//uses-permission")
for p in permissions
	name=p.attributes["android:name"]
	puts "#{name}"
end
