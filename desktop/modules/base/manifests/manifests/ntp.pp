class base::ntp {
	class { '::ntp':
		servers => [ '10.129.1.14', '10.129.1.21' ],
		iburst_enable => true,
		minpoll => '4',
		maxpoll => '4',	
	}
}
