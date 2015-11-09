class base::sudoers {
  class { '::sudo':
    config_file_replace => false,
    if $::operatingsystem == 'Suse' {
      file { '/etc/mft':
        ensure => file,
        mode => '0644',
      }
    }
  }
  sudo::conf { 'ITAdmin':
    priority => 1,
    content  => "%ITAdmin ALL = (ALL) NOPASSWD:/bin/su -"
  }
  sudo::conf { 'appsupport':
    priority => 2,
    content  => "%appsupport ALL = (ALL) NOPASSWD:/bin/su  - epoch,/bin/su - postgres",
  }
  sudo::conf { 'epoch':
    priority => 3,
    content  => "epoch ALL = (ALL) NOPASSWD:/opt/epoch/bin/tshark -i em1,/opt/epoch/bin/tcpdump ,/usr/bin/pkill tcpdump,/usr/bin/cset"
  }
  sudo::conf { 'developer':
    priority => 4,
    content  => "%developer ALL = (ALL) NOPASSWD:/bin/su - epoch"
  }
  sudo::conf { 'MFT':
    priority => 5,
    content  => "%MFT ALL = (ALL) NOPASSWD:/bin/su - mft"
  }
  sudo::conf { 'er':
    priority => 6,
    content  => "%er ALL = (ALL) NOPASSWD:/bin/su - er"
  }
  sudo::conf { 'rdb':
    priority => 7,
    content  => "%rdb ALL = (ALL) NOPASSWD:/bin/su - rdb"
  }
  sudo::conf { 'fcs':
    priority => 8,
    content  => "%fcs ALL = (ALL) NOPASSWD:/bin/su - fcs"
  }
  sudo::conf { 'fst':
    priority => 9,
    content  => "%fst ALL = (ALL) NOPASSWD:/bin/su - fst"
  }
  sudo::conf { 'epcfg':
    priority => 10,
    content  => "%epcfg ALL = (ALL) NOPASSWD:/bin/su - epcfg"
  }
}
