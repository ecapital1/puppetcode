class site::snmpclient {
include ::snmp::client

	class 	{ 'snmp::client':
		manage_client 	=> true,
		agentaddress 	=> [ 'udp:161', ],
		ro_community 	=> '3p0chadmin',
	}
}
