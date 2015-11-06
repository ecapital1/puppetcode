class base::sysctl {
  file {"/etc/sysctl.conf":
    ensure  => present,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    file    => 'base/sysctl.conf',
    notify  => exec['refresh'],
    }
    exec {"refresh":
      command   => "sysctl -p",
  }
}
