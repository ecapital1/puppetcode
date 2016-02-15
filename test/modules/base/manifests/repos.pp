class base::repos {
	case $::osfamily {
	'Suse': {
		case $::operatingsystemrelease {
			'11.3', '12.1': {
						zypprepo { 'SLES12SP1DVD1':
							baseurl					=> 'ftp://10.10.10.81/SLES-12-SP1/DVD1',
							enabled					=> 1,
							autorefresh			=> 1,
							name						=> 'SLES12SP1DVD1',
							path						=> '/',
							type						=> yast2,
							keeppackages		=> 0,
						}
						zypprepo { 'SLES12SP1DVD2':
							baseurl         => 'ftp://10.10.10.81/SLES-12-SP1/DVD2',
							enabled         => 1,
							autorefresh     => 1,
							name            => 'SLES12SP1DVD2',
							path            => '/',
							type            => yast2,
							keeppackages    => 0,
						}
						zypprepo { 'SLES12SDKSP1DVD1':
							baseurl					=> 'ftp://10.10.10.81/SLES-12-SDK-SP1/DVD1',
							enabled					=> 1,
							autorefresh			=> 1,
							name						=> 'SLES12SDKSP1DVD1',
							path						=> '/',
							type						=> yast2,
							keeppackages		=> 0,
						}
						zypprepo { 'SLES12SDKSP1DVD2':
							baseurl         => 'ftp://10.10.10.81/SLES-12-SDK-SP1/DVD2',
							enabled         => 1,
							autorefresh     => 1,
							name            => 'SLES12SDKSP1DVD2',
							path            => '/',
							type            => yast2,
							keeppackages    => 0,
						}
						zypprepo { 'Epoch-Repo':
							baseurl         => 'ftp://10.10.10.81/Epoch-Repo',
							enabled         => 1,
							autorefresh     => 1,
							gpgcheck				=> 0,
							name            => 'Epoch-Repo',
							path            => '/',
							type            => rpm-md,
							keeppackages    => 0,
					}
				}
			}
		}
	}
}
