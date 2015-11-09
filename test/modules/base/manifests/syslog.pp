class base::syslog {
  class { '::rsyslog::client':
    remote_server => [
    {
      host    => '10.10.10.5',
      port    => '514',
      pattern => 'local2.*'
    }
    ]
  }
}
