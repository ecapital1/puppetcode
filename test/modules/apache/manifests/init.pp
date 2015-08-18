class apache {
	package { 'apache2':
		ensure => present,
	}

	file { '/var/www/html':
		ensure 	=> directory,
		owner 	=> root,
		group	=> root,
		mode	=>'0755',
	}	
	
	file { '/var/www/html/index.html':
		ensure 	=> file,
		owner	=> root,
		group	=> root,
		mode	=> '0664',
		source	=> 'puppet:///modules/apache/index.html',
	}
	
	service { 'apache2':
		ensure	=> running,
		enable	=> true,
	}
}
