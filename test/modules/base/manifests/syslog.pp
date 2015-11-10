class base::syslog {
  class { '::rsyslog::client':
    log_remote                => true,
    spool_size                => '1g',
    spool_timeoutenqueue      => false,
    remote_type               => 'tcp',
    remote_forward_format     => 'RSYSLOG_ForwardFormat',
    log_local                 => false,
    log_auth_local            => false,
    listen_localhost          => false,
    split_config              => false,
    custom_config             => undef,
    custom_params             => undef,
    server                    => 'log',
    port                      => '514',
    ssl_ca                    => undef,
    ssl_permitted_peer        => undef,
    ssl_auth_mode             => 'anon',
    log_templates             => false,
    actionfiletemplate        => false,
    high_precision_timestamps => false,
    rate_limit_burst          => undef,
    rate_limit_interval       => undef,
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
