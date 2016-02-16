class base::ssh {
  class { '::ssh':
    server_options => {
      'Port' => [22, 2222],
    }
  }
}
