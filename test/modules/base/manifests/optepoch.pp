class base::optepoch {
  rsync::get { "/opt/epoch/":
    user    => 'rsync',
    source  => 'puppet:/opt/epoch/',
    #recurse => true,
  }
}
