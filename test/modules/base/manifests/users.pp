#class base::users {
#    accounts::user { 'epoch':
#    }
#}
accounts::user { 'jeff':
  shell    => '/bin/zsh',
  comment  => 'Jeff McCune',
  groups   => [
    'admin',
    'sudonopw',
  ],
  uid      => 1112,
  gid      => 1112,
  locked   => true,
  sshkeys  => [
    'ssh-rsa AAAA...',
    'ssh-dss AAAA...',
  ],
  password => '!!',
}
