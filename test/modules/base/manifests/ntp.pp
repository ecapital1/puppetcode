class base::ntp {
	class { '::ntp':
		servers => [ $ntplocation ],
		iburst_enable => true,
		minpoll => '4',
		maxpoll => '4',
	}
}
