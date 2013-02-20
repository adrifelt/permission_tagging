
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

God.watch do |w|
  w.name = "APK Check"
  w.log = '/Users/Jonathan/Desktop/eecs350/myprocess.log'


  w.start = "ruby /Users/Jonathan/Desktop/eecs350/permission_upload.rb"
  w.start_if do |start|
    start.condition(:process_running) do |c|
      c.interval = 60.seconds
      c.running = false
    end
  end
  w.transition(:up, :start) do |on|
    on.condition(:process_exits) do |c|
      c.notify = 'developers'
    end
  end
end
