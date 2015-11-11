class base::packages {
    $packages = hiera('packages')
    $packages.each |String $package1|{
      package { '$package1':
        ensure => installed,
    }
  }
}
