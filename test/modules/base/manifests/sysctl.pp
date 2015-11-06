class base::sysctl {
  file {"/etc/sysctl.conf":
    ensure  => present,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    template    => 'base/sysctl.erb',
    notify  => Exec['sysctl_refresh'],
    }
    exec {"sysctl_refresh":
      command   => "sysctl -p",
  }
}
