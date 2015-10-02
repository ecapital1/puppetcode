class base::repos {
	case $::osfamily {
	'Suse': {
		case $::operatingsystemrelease {
			'11.3': {
					zypprepo { 'SLES11SP3DVD1':
						baseurl					=> 'ftp://10.10.10.81/SLES-11-SP3/DVD1',
						enabled					=> 1,
						autorefresh			=> 1,
						name						=> 'SLES11SP3DVD1',
						path						=> '/',
						type						=> yast2,
						keeppackages		=> 0,
					}
					zypprepo { 'SLES11SP3DVD2':
    				baseurl         => 'ftp://10.10.10.81/SLES-11-SP3/DVD2',
    				enabled         => 1,
    				autorefresh     => 1,
    				name            => 'SLES11SP3DVD2',
    				path            => '/',
    				type            => yast2,
    				keeppackages    => 0,
					}
					zypprepo { 'SLE11SP3SDKDVD1':
						baseurl					=> 'ftp://10.10.10.81/SLE-11-SP3-SDK/DVD1',
						enabled					=> 1,
						autorefresh			=> 1,
						name						=> 'SLE11SP3SDKDVD1',
						path						=> '/',
						type						=> yast2,
						keeppackages		=> 0,
					}
					zypprepo { 'SLES11SP3DVD2':
    				baseurl         => 'ftp://10.10.10.81/SLE-11-SP3-SDK/DVD2',
    				enabled         => 1,
    				autorefresh     => 1,
    				name            => 'SLE11SP3SDKDVD2',
    				path            => '/',
    				type            => yast2,
    				keeppackages    => 0,
					}
					zypprepo { 'SLE11SP3SDKDVD1':
						baseurl					=> 'ftp://10.10.10.81/SLE-11-RT-SP3/DVD1',
						enabled					=> 1,
						autorefresh			=> 1,
						name						=> 'SLE11SP3RTDVD1',
						path						=> '/',
						type						=> yast2,
						keeppackages		=> 0,
					}
					zypprepo { 'SLES11SP3DVD2':
    				baseurl         => 'ftp://10.10.10.81/SLE-11-RT-SP3/DVD2',
    				enabled         => 1,
    				autorefresh     => 1,
    				name            => 'SLE11SP3RTDVD2',
    				path            => '/',
    				type            => yast2,
    				keeppackages    => 0,
					}
				}
			'12.0': {
						zypprepo { 'SLES12DVD1':
							baseurl					=> 'ftp://10.10.10.81/SLES-12/DVD1',
							enabled					=> 1,
							autorefresh			=> 1,
							name						=> 'SLES12DVD1',
							path						=> '/',
							type						=> yast2,
							keeppackages		=> 0,
						}
						zypprepo { 'SLES12DVD2':
							baseurl         => 'ftp://10.10.10.81/SLES-12/DVD2',
							enabled         => 1,
							autorefresh     => 1,
							name            => 'SLES12DVD2',
							path            => '/',
							type            => yast2,
							keeppackages    => 0,
						}
						zypprepo { 'SLES12SDKDVD1':
							baseurl					=> 'ftp://10.10.10.81/SLES-12-SDK/DVD1',
							enabled					=> 1,
							autorefresh			=> 1,
							name						=> 'SLES12SDKDVD1',
							path						=> '/',
							type						=> yast2,
							keeppackages		=> 0,
						}
						zypprepo { 'SLES12SDKDVD2':
							baseurl         => 'ftp://10.10.10.81/SLES-12-SDK/DVD2',
							enabled         => 1,
							autorefresh     => 1,
							name            => 'SLES12SDKDVD2',
							path            => '/',
							type            => yast2,
							keeppackages    => 0,
						}
					}
			}
		}
	}
}
