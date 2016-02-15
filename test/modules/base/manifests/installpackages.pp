class base::installpackages {
  notice ("install packages running on $::osfamily and on $::operatingsystemrelease")
  $ospackages = hiera_array('ospackages')
  #$ospackages.each |String $packages|{
  package {$ospackages:
    ensure => installed,
  }
}
