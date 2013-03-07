require 'rubygems'
require 'calais'
require 'json'
require 'pry'
require 'nokogiri'
require 'active_support/all'
keys = 'nwkm52bfj4dtf92m46n8vedf'


file = File.open("json_output.txt")
c = file.read
c = c.scan(/[[:print:]]/).join
contents = JSON.parse(c)

contents.each do |key, value|
  puts key + ".apk\n"
  values = []
  results = Calais.enlighten(:content => value, :content_type => :raw, :license_id => keys)
  if not results.nil?
      a = Hash.from_xml(results)
      o = a.to_s.match(/categoryName\"=>\"\w*/)
      if not o.nil?
        puts o[0].gsub(/categoryName\"=>\"/, '') + "\n"
      end
  end
  puts "\n"
end


# puts values.to_json