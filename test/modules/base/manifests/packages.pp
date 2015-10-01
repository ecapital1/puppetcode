class base::packages {
  $repodir = "/etc/zypp/repos.d"
  $repofiles = [ "$repodir/SLES11SP3DVD1.repo","$repodir/SLES11SP3DVD2.repo" ]
  $sourcedir = "puppet:///modules/base/sles/11sp3/"
  $sourcefile = [ "sles11sp3dvd1","sles11sp3dvd2"]
  $repofiles.each |String $repofiles|{
  file { $repofiles:
    ensure => "present",
    owner => "root",
    group => "root",
    mode => 0644,
    source => $sourcefile.each |String $sourcefile| {"$sourcedir/$sourcefile"}
  }
}
  $packages = hiera("packages")
  $packages.each |String $packages|{
  	package { "$packages":
    	ensure => installed,
  	}
  }
}
