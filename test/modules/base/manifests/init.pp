class base {
	include base::repos
	include base::dellrepo
	#include base::python
	include base::snmp
	include base::ntp
	include base::installpackages
	include base::sysctl
	include base::sudoers
	include base::dns
	include base::syslog
	include base::ssh
	include base::sssd
	#include base::users
	case $hostname {
		'epcau-srv-research': {
			include base::mounts
			include base::optepoch
		}
		'epose-srv-003': {
			include base::optepoch
		}
		default: {
			notice("only for selected servers")
		}
	}
}
