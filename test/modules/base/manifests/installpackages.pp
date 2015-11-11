class base::installpackages {
    $packagelist = hiera('ospackages')
    $packagelist.each |String $packagelist|{
    #  package { '$packagelist1':
    #    ensure => installed,
    #}
  }
}
