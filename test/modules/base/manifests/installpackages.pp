class base::installpackages {
    $packagelist = hiera('ospackages')
    $packagelist.each |String $packagelist1a|{
      package { '$packagelist1':
        ensure => installed,
    }
  }
}
