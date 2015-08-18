class snmp::snmp {
	class { '::snmp':
		manage_client 	=> true,
		agentaddress 	=> [ 'udp:161', ],
		ro_community 	=> '3p0chadmin',
	}
}
