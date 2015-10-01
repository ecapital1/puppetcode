class base::packages {
  file {'/etc/zypp/repo.d/SUSE_Linux_Enterprise_Server_11_SP3.repo':
    ensure => present,
    content => template('/base/sles/11sp3/sles11sp3dvd1.erb')
}
  $packages = hiera("packages")
  $packages.each |String $packages|{
  	package { "$packages":
    	ensure => installed,
  	}
  }
}
