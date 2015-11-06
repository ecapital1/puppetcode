class base::sysctl {
  file {"/etc/sysctl.conf":
    ensure  => present,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => file("base/sysctl.conf"),
    notify  => Exec['sysctl_refresh'],
    }
    exec {"sysctl_refresh":
      path      => '/sbin',
      command   => "sysctl -p",
  }
}
