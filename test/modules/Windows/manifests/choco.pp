class windows::choco {
  case $::osfamily {
    'windows': {
      class { '::choclatey:'}
    }
  }
}
