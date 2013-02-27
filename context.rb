require 'rubygems'
require 'alchemy_api'
require 'json'

AlchemyAPI.key = "bfc9f1c85f548d2ee9272e49ad3866f0e663cef1"

file = File.open("results/json.txt")
c = file.read
c = c.scan(/[[:print:]]/).join
contents = JSON.parse(c)

results = []

contents.each do |key, value|
  result = AlchemyAPI.search(:keyword_extraction, :text => value)
  # result = AlchemyAPI.search(:text_extraction, :text => value)
  # :term_extraction
  # :concept_tagging

  results << [key, result.to_json]
end


puts results.to_json