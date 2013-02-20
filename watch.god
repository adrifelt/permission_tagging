God.watch do |w|
  w.name = "APK Check"
  w.start = "ruby /Users/Jonathan/Desktop/eecs350/permission_upload.rb > output.txt"
end

God::Contacts::Email.defaults do |d|
  d.from_email = 'watcher@eecs350.com'
  d.from_name = 'God'
  d.delivery_method = :sendmail
end

God.contact(:email) do |c|
  c.name = 'Jon'
  c.group = 'developers'
  c.to_email = 'friedmanj98@gmail.com'
end

God.contact(:email) do |c|
  c.name = 'Zhengyang'
  c.group = 'developers'
  c.to_email = 'ZhengyangQu2017@u.northwestern.edu'
end


God.contact(:email) do |c|
  c.name = 'Peng'
  c.group = 'developers'
  c.to_email = 'PengXu2012@u.northwestern.edu'
end

