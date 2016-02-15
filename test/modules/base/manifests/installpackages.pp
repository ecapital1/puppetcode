class base::installpackages {
    notice ("install package running on $::osfamily and on $::operatingsystemrelease")
    ['a', 'b', 'c'].each{#hiera_array('ospackages')
      notice "working"
      #package { $package:
      #  ensure => installed,
      #}
    }
    file {"/var/run/bacula/":
      ensure => 'directory',
    }
}
