class base::syslog {
  class { '::rsyslog::client':
      server => '10.10.10.5',
      port    => '514',
      #pattern => 'local2.*'
      #content       => template
      #custom_config => template('rsyslog/client/remote.conf.erb'),
      #custom_config => template('base/rsyslog.conf.erb'),
  }
}
