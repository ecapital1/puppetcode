class base::installpackages {
    notice ("install package running on $::osfamily and on $::operatingsystemrelease")
    $packages = hiera_array('ospackages')
    $packages.each |$package| {
      package { $package:
        ensure => installed,
      }
    }
    file {"/var/run/bacula/":
      ensure => 'directory',
    }
}
