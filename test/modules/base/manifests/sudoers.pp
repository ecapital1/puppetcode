class base::sudoers {
  class { '::sudo':
    config_file_replace => false,
  }
  sudo::conf { 'ITAdmin':
    priority => 1,
    content  => "%ITAdmin ALL = (ALL) NOPASSWD:/bin/su -"
  }
  sudo::conf { 'appsupport':
    priority => 2,
    content  => "%appsupport ALL = (ALL) NOPASSWD:/bin/su  - epoch,/bin/su - postgres",
  }
  sudo::conf { 'developer':
    priority => 3,
    content  => "%developer ALL = (ALL) NOPASSWD:/bin/su - epoch"
  }
}
