class base::installpackages {
    $packages = hiera_array('ospackages')
    $packages.each |String $packages|{
      notify {"the package is: $packages":}
      package { $packages:
      ensure => installed,
      }
    }
}
