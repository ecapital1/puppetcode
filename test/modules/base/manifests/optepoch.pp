class base::optepoch {
  rsync::get { "$hostname:/opt/epoch/":
    user    => 'root',
    keyfile => '/root/.ssh/id_rsa',
    source  => 'puppet:/opt/epoch/',
    #recurse => true,
  }
}
