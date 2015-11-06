class base::sysctl {
  sysctl { 'net.ipv4.icmp_echo_ignore_broadcasts': value => '1' }
}
