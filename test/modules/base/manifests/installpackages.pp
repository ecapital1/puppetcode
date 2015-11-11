class base::installpackages {
    $packagelist = hiera('ospackages')
    $packagelist.each |String $packagelist|{
      package { 'name':
        ensure => installed,
      }
    }
}
