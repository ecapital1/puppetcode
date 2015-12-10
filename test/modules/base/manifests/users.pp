class base::users {
  class { '::accounts':
      account => {'epoch':
        shell    => '/bin/bash',
      }
  }
}
