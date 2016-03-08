class base::syslog {
  class { '::rsyslog::params':
    perm_file => '0644',
  }
  class { '::rsyslog::client':
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
