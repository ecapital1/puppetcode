# role.rb
Facter.add('role') do
  setcode 'contents = File.readlines("/etc/role")'
end
