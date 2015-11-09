class base::dns {
  class { '::dnsclient':
    nameservers => '10.10.10.2, 10.129.1.21',
    domain      => 'epochcapital.com.au',
    search      => 'epochcapital.com.au'
  }
}
