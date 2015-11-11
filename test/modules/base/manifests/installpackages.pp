class base::installpackages {
    $packages = hiera_array('ospackages')
    $packages.each |String $packages|{
      notify {"the package is: $packages":}
    #  package { 'name':
    #    ensure => installed,
    #  }
    }
}
