class base::installpackages {
  $packages = hiera_array('ospackages')
  $packages.each |$index, $packages|{
    package { $packages:
      ensure => installed,
    }
  }
}
