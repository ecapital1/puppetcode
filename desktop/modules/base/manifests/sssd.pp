class base::sssd {
  class { '::sssd':
    config => {
      'sssd' => {
        'config_file_version' => '2',
        'services' => [ 'nss','pam' ],
        'domains'  => 'LDAP',
        },
      'domain/LDAP' => {
        'ldap_uri'                => 'ldap://10.10.10.14',
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
        'simple_allow_groups'     => hiera ('sssd_simple_allow_groups'),
        'simple_allow_users'      => hiera ('sssd_simple_allow_users'),
        },
      }
    }
    case $operatingsystem {
      'Ubuntu': {
        file { "/usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf":
          ensure  => present,
          owner   => 'root',
          group   => 'root',
          mode    => '0644',
          content => file("base/50-ubuntu.conf"),
      }
    }
  }
  }
