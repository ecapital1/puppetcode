class base::optepoch {
  rsync::put { "/opt/epoch/":
    #ensure  => 'directory',
    source  => 'puppet:///opt_epoch/',
    #recurse => true,
  }
}
