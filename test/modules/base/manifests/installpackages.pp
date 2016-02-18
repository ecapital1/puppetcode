class base::installpackages {
  notice ("install packages running on $::osfamily and on $::operatingsystemrelease")
  $ospackages = hiera_array('ospackages')
  package {$ospackages:
    ensure => installed,
  }
  file {"/var/run/bacula/":
      ensure => 'directory',
    }
  file {"/Data/rdb":
      ensure  => 'directory',
    }
}
