# site.rb
Facter.add('site') do
  setcode do
    Facter::Core::Execution.exec("/bin/hostname hostname | cut -d '-' -f1")
  end
end
