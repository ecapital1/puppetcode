class base::sssd {
  class { '::sssd':
    config => {
      'sssd' => {
        'key1' => 'value1',
        'keyX' => [ 'valueY', 'valueZ' ],
        },
      'domain/LDAP' => {
        'key2' => 'value2',
        },
      }
    }
  }
