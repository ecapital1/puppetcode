class base::dns {
  class { '::dnsclient':
    nameservers => [hiera('dnslocation')],
    domain      => 'epochcapital.com.au',
    search      => 'epochcapital.com.au',
    options     => ['timeout:1']
  }
}
