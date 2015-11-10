class base::syslog {
  class { '::rsyslog::client':
      server => '10.10.10.5',
      port    => '514',
    #  pattern => 'local2.*'
      custom_config => 'rsyslog/client/remote.conf.erb'
  }
}
