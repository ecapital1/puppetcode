class windowsbase::windowsupdate {

file { 'c:/puppetscripts/Run-WindowsUpdate.ps1':
  ensure => file,
  mode => '0660',
  owner => 'admin',
  group => 'Administrators',
  source => "puppet:///modules/windowsbase/Run-WindowsUpdate.ps1",
  }

scheduled_task { 'windowsupdate':
      ensure    => present,
      enabled   => true,
      command   => 'c:/puppetscripts/Run-WindowsUpdate.ps1',
      provider  => powershell,
      #arguments => '/flags /to /pass',
      trigger   => {
        schedule   => monthly,
        every      => 1,
        start_date => '2015-11-30',
        start_time => '08:00',
      }
  }

  reboot {'after update':
      subscribe => scheduled_task['windowsupdate'],
    }
  }
