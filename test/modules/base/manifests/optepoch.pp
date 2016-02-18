class base::optepoch {
  file { "/opt/epoch/":
    ensure  => 'directory',
    source  => 'file:///opt_epoch/',
    recurse => true,
  }
}
