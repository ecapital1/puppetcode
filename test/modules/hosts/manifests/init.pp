class host {
	host { 'puppettest.epochcapital.com.au':
		ensure  => present,
		ip 	=> '127.0.0.1',
	}
}
