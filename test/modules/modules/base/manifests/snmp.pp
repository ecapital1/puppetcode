class base::snmp {
	include ::snmp::client
	class { '::snmp':
		agentaddress => ['udp:161'],
		ro_community => '3p0chSNMP',
	}
}
