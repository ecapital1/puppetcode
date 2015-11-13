class windows::choco {
  case $::operatingsystem {
    'windows': {
      class { '::choclatey:'}
    }
  }
}
