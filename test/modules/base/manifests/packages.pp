class base::packages {
    $package = hiera('packages')
    $package.each |String $package|{
  	  package { "$package":
    	  ensure => installed,
    }
  }
}
