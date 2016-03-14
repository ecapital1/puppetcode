class base::installpackages {
  notice ("install packages running on $::osfamily and on $::operatingsystemrelease")
  $ospackages = hiera_array('ubuntuospackages')
  package {$ospackages:
    ensure => installed,
  }
  file {"/var/run/bacula/":
      ensure => 'directory',
    }
}
