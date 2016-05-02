class base::ntp {
	notify { $::role: }
	notify { $::site: }
	class { '::ntp':
		servers => [ hiera('ntplocation') ],
		iburst_enable => true,
		minpoll => '4',
		maxpoll => '4',
	}
}
