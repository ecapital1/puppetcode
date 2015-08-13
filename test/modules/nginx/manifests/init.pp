class nginx {
	package { 'nginx':
		ensure => present,
	}

	file { '/var/www':
		ensure 	=> directory,
		owner 	=> root,
		group	=> root,
		mode	=>'0755',
	}	
	
	file { '/var/www/index.html':
		ensure 	=> file,
		owner	=> root,
		group	=> root,
		mode	=> '0664'
		source	=> 'puppet:///modules/nginx/index.html',
	}
}
