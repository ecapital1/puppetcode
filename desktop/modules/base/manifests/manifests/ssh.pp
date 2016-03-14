class base::ssh {
  class { '::ssh':
    server_options => {
      'Port' => [22, 2222],
      'ClientAliveInterval' => 30,
      'TCPKeepAlive' => yes,
      'ClientAliveCountMax' => 99999,
    }
  }
}
