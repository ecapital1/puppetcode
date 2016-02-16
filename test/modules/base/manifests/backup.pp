class base::backup {
  file {"/etc/bacula/bacula-fd.conf":
    ensure  => present,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => file("base/bacula-fd.conf"),
    #notify  => Exec['sysctl_refresh'],
    }

}
