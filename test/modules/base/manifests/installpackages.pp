class base::installpackages {
    $packagelist = hiera('ospackages')
    $packagelist.each |String $packagelist1|{
      package { '$packagelist1':
        ensure => installed,
    }
  }
}
