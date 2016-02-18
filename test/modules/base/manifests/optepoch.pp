class base::optepoch {
  file { "/opt/epoch/":
    ensure  => 'directory',
    source  => 'puppet:///opt_epoch/',
    recurse => true,
    timeout => 1800,
  }
}
