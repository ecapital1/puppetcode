class base::ntp {
	class { '::ntp':
		case $::hostname{
			'alc-srv-011':{
				servers => [ '10.251.25.108', '10.251.25.109' ],
				iburst_enable => true,
				minpoll => '4',
				maxpoll => '4',
		}
			default {
				servers => [ '10.129.1.14', '10.129.1.21' ],
				iburst_enable => true,
				minpoll => '4',
				maxpoll => '4',
			}
		}
	}
}
