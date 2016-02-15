class base::installpackages {
  $packages = hiera_array('ospackages')
  $package = each($packages){
    package { $package:
      ensure => installed,
    }
  }
}
