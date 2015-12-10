#class base::users {
#    accounts::user { 'epoch':
#    }
#}
accounts::user { 'jeff':
  shell    => '/bin/zsh',
  comment  => 'Jeff McCune',
  groups   => [
    'admin',
  ],
  locked   => true,
}
