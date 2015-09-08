class sssd {'::sssd':
  config => {
    'sssd' => {
      'domains'             => 'epochcapital.com.au',
      'config_file_version' => 2,
      'services'            => ['nss', 'pam'],
    }
    'domain/epochcapital.com.au' => {
      'ad_domain'                      => 'epochcapital.com.au',
      'ad_server'                      => ['10.10.10.14'],
      'cache_credentials'              => true,
      'default_shell'                  => '/bin/bash',
      'ldap_id_mapping'                => false,
      'use_fully_qualified_names'      => false,
      'fallback_homedir'               => '/home/%d/%u',
      'access_provider'                => 'simple',
      'simple_allow_groups'            => ['admins', 'users'],
    }
  }
}
