class base::sssd {
  class { '::sssd':
    config => {
      'sssd' => {
        'config_file_version' => '2',
        'services' => [ 'nss', 'pam' ],
        'domains'  => 'LDAP',
        },
      'domain/LDAP' => {
        'ldap_uri'                => 'ldap://10.10.10.147',
        'ldap_search_base'        => 'dc=epochcapital,dc=com,dc=au',
        'ldap_schema'             => 'rfc2307',
        'id_provider'             => 'ldap',
        'ldap_user_uuid'          => 'entryuuid',
        'ldap_group_uuid'         => 'entryuuid',
        'ldap_tls_reqcert'        => 'never',
        'ldap_id_use_start_tls'   => 'False',
        'enumerate'               => 'True',
        'cache_credentials'       => 'True',
        'chpass_provider'         => 'ldap',
        'auth_provider'           => 'ldap',
        'access_provider'         => 'simple',
        'simple_allow_groups'     => 'ITAdmin, appsupport, developer',
        'simple_allow_users'      => 'epoch, appsupport',
        },
      }
    }
  }
