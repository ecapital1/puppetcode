class base::repos {
	case $::osfamily {
	'Suse': {
		case $::operatingsystemrelease {
			'11.3', '12.0': {
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
						zypprepo { 'Epoch-Repo':
							baseurl         => 'ftp://10.10.10.81/Epoch-Repo',
							enabled         => 1,
							autorefresh     => 1,
							name            => 'Epoch-Repo',
							path            => '/',
							type            => yast2,
							keeppackages    => 0,
					}
			}
		}
	}
}
