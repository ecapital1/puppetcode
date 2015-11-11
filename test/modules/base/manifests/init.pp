class base {
	include base::repos
	include base::dellrepo
	#include base::python
	#include base::snmp
	#include base::ntp
	#include base::packages
	#include base::sysctl
	#include base::sudoers
	#include base::dns
	#include base::syslog
	#include base::ssh
}
