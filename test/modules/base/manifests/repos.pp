class base::repos {
	zypprepo { 'SLES11SP3DVD1':
		baseurl		=> 'ftp://10.10.10.81/SLES-11-SP3/DVD1',
		enabled		=> 1,
		autorefresh	=> 1,
		name		=> 'SLES11SP3DVD1',
		path		=> '/',
		type		=> yast2,
		keeppackages	=> 0,
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
}
