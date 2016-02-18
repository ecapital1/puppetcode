class base::optepoch {
  file { "/opt/epoch/":
    ensure  => 'directory',
    source  => 'file:///opt/epoch/',
    recurse => true,
  }
}
