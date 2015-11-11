class base::packages {
    $packages = hiera("packages")
    $packages.each |String $packages|{
  	  package { "$packages":
    	  ensure => installed,
    }
  }
}
