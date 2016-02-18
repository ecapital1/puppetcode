class base::optepoch {
  rsync::put { "/opt/epoch/":
    user    => 'root',
    keyfile => '/root/.ssh/authorized_keys',
    source  => 'puppet:///opt_epoch/',
    #recurse => true,
  }
}
