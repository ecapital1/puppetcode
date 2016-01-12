class base::snmp {
	class { '::snmp':
		agentaddress => ['udp:161'],
		ro_community => hiera('snmp.community'),
		ro_network	 => ('10.10.10.5'),
		openmanage_enable => true,
        }
}
