class base::installpackages {
  $packages = hiera_array('ospackages')
  each($packages)#{
    #package { $package:
    #  ensure => installed,
    #}
  }
}
