class base::users {
    class { '::accounts::user':
      { 'epoch':
        shell   => '/bin/bash',
      }
    }
}
