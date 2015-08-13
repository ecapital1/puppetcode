package { 'openssh':
	ensure => present,
}

service { 'sshd':
	ensure => running,
	enable => true,
	require => Package['openssh'],
}
