class base::syslog {
  class { '::rsyslog::client':
    perm_file => '0644',
    remote_servers => [{
      host => '10.10.10.5',
      port    => '514',
      pattern => 'local2.*',
    },
    {
      host => '10.10.10.5',
      port    => '514',
      pattern => 'local3.*',
    }
    ]
  }
}
