class base::installpackages {
  #$data = ["routers", "servers", "workstations"]
["routers", "servers", "workstations"].each |$item| {
    notify { $item:
      message => $item
    }
  }
#  $packages = hiera_array('ospackages')
#  $packages.each |$index, $packages|{
#    package { $packages:
#      ensure => installed,
#    }
#  }
}
