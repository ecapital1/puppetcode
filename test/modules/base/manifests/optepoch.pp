class base::optepoch {
  file { "/opt/epoch/":
    ensure  => 'directory',
    source  => 'puppet:///epcau-srv-dev:/opt/epoch',
    recurse => true,
  }
}
