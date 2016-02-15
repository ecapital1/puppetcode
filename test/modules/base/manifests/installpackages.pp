class base::installpackages {
  $packages = hiera_array('ospackages')
  $packages.each |String $packages|{
    package { $packages:
      ensure => installed,
    }
  }
}
