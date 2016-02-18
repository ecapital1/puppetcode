class base::optepoch {
  rsync::put { "/opt/epoch/":
    user    => 'root',
    source  => 'puppet:///opt_epoch/',
    #recurse => true,
  }
}
