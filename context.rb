require 'rubygems'
require 'alchemy_api'
require 'json'
require 'pry'

AlchemyAPI.key =
['bfc9f1c85f548d2ee9272e49ad3866f0e663cef1',
'4315f947e2ea43c6f2560f048ed25ac585efd94a',
'd16d4ef723dce3523f2a85d108a5e903fd0c70c9',
'7aead646c8e2af56ce7477054f5b9405c22ffe2d'].sample(1).first

# extra keys
# 'bfc9f1c85f548d2ee9272e49ad3866f0e663cef1'
# '4315f947e2ea43c6f2560f048ed25ac585efd94a'
# 'd16d4ef723dce3523f2a85d108a5e903fd0c70c9'
# '7aead646c8e2af56ce7477054f5b9405c22ffe2d'

file = File.open("results/json.txt")
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
  end
  puts "\n"
end


# puts values.to_json