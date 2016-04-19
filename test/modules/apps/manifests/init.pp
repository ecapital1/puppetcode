class apps {
  case $hostname {
    'epcau-srv-postgres': {
      include postgres.pp
    }
    default: {
      # code
    }
  }
  }
}
