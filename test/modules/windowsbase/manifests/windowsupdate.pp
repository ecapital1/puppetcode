class windowsbase::windowsupdate {

file { 'c:/puppetscripts/winupdate.ps1':
  ensure => file,
  mode => '0660',
  owner => 'admin',
  group => 'Administrators',
  source => "puppet:///modules/windowsbase/winupdate.ps1",
  }

scheduled_task { 'windowsupdate':
      ensure    => present,
      enabled   => true,
      command   => 'c:/puppetscripts/winupdate.ps1',
      provider  => powershell,
      #arguments => '/flags /to /pass',
      trigger   => {
        schedule   => daily,
        every      => 1,
        start_date => '2016-01-11',
        start_time => '08:00',
      }
  }

  reboot {'after update':
      subscribe => scheduled_task['windowsupdate'],
    }
  }
