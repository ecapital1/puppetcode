class base::ntp {
	class { '::ntp':
		servers => [ hiera('ntplocation.1') ],
		iburst_enable => true,
		minpoll => '4',
		maxpoll => '4',
	}
}
