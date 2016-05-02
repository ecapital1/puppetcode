# site.rb
Facter.add('site') do
  setcode '/bin/hostname | cut -d - -f1'
end
