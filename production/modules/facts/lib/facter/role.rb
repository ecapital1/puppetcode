# role.rb
Facter.add('role') do
  setcode 'cat /etc/role'
end
