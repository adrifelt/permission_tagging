require 'rubygems'
require 'watir-webdriver'

client = Selenium::WebDriver::Remote::Http::Default.new
client.timeout = 3000 # seconds – default is 60

b = Watir::Browser.new :firefox, :http_client => client
b.goto 'http://www.android-permissions.org/'

#put your directory here
entries = Dir.entries("/Users/Jonathan/Desktop/eecs350/apps")

entries.each do |entry|
  unless entry == "." || entry == ".." || entry == ".DS_Store"
    b.goto("http://www.android-permissions.org/")
    b.link(:class, "important").click
    b.file_field(:id, "file").set("/Users/Jonathan/Desktop/eecs350/apps/" + entry)
    b.button(:name, "submit").click
    text = b.div(:id, "outermost").text
    puts entry + "\n"
    puts text
    puts "\n"
  end
end

