class base::packages {
  $packages = heira_array('packages'),
  package { '$packages':
    ensure => installed,
  }
}
