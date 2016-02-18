class base::optepoch {
  rsync::put { "$hostname:/opt/epoch/":
    user    => 'root',
    keyfile => '/root/.ssh/id_rsa',
    source  => 'puppet:///opt_epoch/',
    #recurse => true,
  }
}
