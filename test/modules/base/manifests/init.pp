class base {
	if $is_virtual {
		notice("This is a VWMARE Host")
		include base::ntp
		include base::sssd
		include base::sudoers
		include base::dns
		include base::sysctl
		include base::ssh
	} else {
	case $operatingsystem {
		'SLES': {
			include base::repos
			include base::dellrepo
			#include base::python
			include base::snmp
			#include base::ntp
			include base::installpackages
			include base::sysctl
			include base::sudoers
			include base::dns
			include base::syslog
			include base::ssh
			include base::sssd
			#include base::users
			include base::optepoch
		}
		'Ubuntu': {
			include base::ntp
		#	include base::installpackages
			include base::sudoers
			include base::dns
			include base::ssh
			include base::sssd
		}
	}
}
	case $hostname {
		'epcau-srv-research': {
			include base::mounts
		}
		default: {
			notice("only for selected servers")
		}
	}
}
