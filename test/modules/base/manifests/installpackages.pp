class base::installpackages {
    $packages = hiera('ospackages')
    $packages.each |String $packages|{
      notify {'packages'}
    #  package { 'name':
    #    ensure => installed,
    #  }
    }
}
