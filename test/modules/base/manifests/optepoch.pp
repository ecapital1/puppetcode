class base::optepoch {
  rsync::get { "/opt/epoch/":
    #ensure  => 'directory',
    source  => 'puppet:///opt_epoch/',
    #recurse => true,
  }
}
