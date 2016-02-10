class base::installpackages {
    notice ("install package running on $::osfamily and on $::operatingsystemrelease")
    $packages = hiera_array('ospackages')
    each($packages) |$packages| {
      package { $packages:
        ensure => installed,
      }
    }
    file {"/var/run/bacula/":
      ensure => 'directory',
    }
}
