class base::installpackages {
  $packages = hiera_array('ospackages'),
  $packages.each#{
    #package { $package:
    #  ensure => installed,
    #}
  #}
}
