require 'rubygems'
require 'alchemy_api'
require 'json'
require 'pry'

keys = ['bfc9f1c85f548d2ee9272e49ad3866f0e663cef1',
'4315f947e2ea43c6f2560f048ed25ac585efd94a',
'd16d4ef723dce3523f2a85d108a5e903fd0c70c9',
'7aead646c8e2af56ce7477054f5b9405c22ffe2d',
'dbe4b3a50e03abe67a7c5296d00ebfe7bf34f7de',
'969682b18e51ed442c6bb62e9646b9ca6d4f3839',
'8dfe30d0dac1fb64d362855d153fddfa17c5b126',
'5e3a835f84b5175389ac5b446ae625af325109e8']
AlchemyAPI.key = keys.sample(1).first


file = File.open("json_output.txt")
c = file.read
c = c.scan(/[[:print:]]/).join
contents = JSON.parse(c)

results = []

contents.each do |key, value|
  puts key + ".apk\n"
  values = []
  result = AlchemyAPI.search(:keyword_extraction, :text => value)
  if not result.nil?
    result.each do |r|
        puts r["text"] + "\n"
        values << r["text"]
    end
  else
    AlchemyAPI.key = keys.sample(1).first
    result = AlchemyAPI.search(:keyword_extraction, :text => value)
    result.each do |r|
      puts r["text"] + "\n"
      values << r["text"]
    end
  end
  sleep(Random.new.rand(1..100) / 100)
  puts "\n"
end


# puts values.to_json