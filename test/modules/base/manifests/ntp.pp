class base::ntp {
	class { '::ntp':
		servers => [ hiera('ntp') ],
		iburst_enable => true,
		minpoll => '4',
		maxpoll => '4',
	}
}
