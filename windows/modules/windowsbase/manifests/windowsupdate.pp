class windowsbase::windowsupdate {

file { 'c:/puppetscripts':
	ensure	=> directory,
	mode	=> '0660',
	owner => 'admin',
  	group => 'Administrators',
}

file { 'c:/puppetscripts/winupdate2.ps1':
  ensure => file,
  mode => '0660',
  owner => 'admin',
  group => 'Administrators',
  source => "puppet:///modules/windowsbase/winupdate2.ps1",
}

exec {"windows_update":
	command	=> 'c:/puppetscripts/winupdate.ps1 y y',
	logoutput	=> true,
	refreshonly	=> true,
	timeout		=> 36000,
	provider => powershell,
}

#scheduled_task { 'windowsupdate':
#      ensure    => present,
#      enabled   => true,
#      command   => 'C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe - file c:/puppetscripts/Run-WindowsUpdate.ps1',
      #arguments => '/flags /to /pass',
#      trigger   => {
#        schedule   => daily,
#        every      => 30,
#        start_date => '2015-12-03',
#        start_time => '15:30',
#      }
#    }
  }
