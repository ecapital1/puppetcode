class base::installpackages {
    notify {"install package running on $::osfamily and on $::operatingsystemrelease"}
    $packages = hiera_array('ospackages')
    $packages.each |String $packages|{
      package { $packages:
        ensure => installed,
      }
    }
}
