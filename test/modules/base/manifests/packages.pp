class base::packages {
    $packages = hiera('packages')
    $packages.each |String $package|{
      package { '$package':
        ensure => installed,
    }
  }
}
