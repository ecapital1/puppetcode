class base::installpackages {
    #notice ("install package running on $::osfamily and on $::operatingsystemrelease");
    #$packages = ['a', 'b', 'c']#hiera_array('ospackages')
    #notice $packages;
    #$packages.each {
    #  notice $package
      #package { $package:
      #  ensure => installed,
      #}
    #}
#    file {"/var/run/bacula/":
#      ensure => 'directory',
#    }
}
