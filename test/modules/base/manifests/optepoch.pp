class base::optepoch {
  rsync::get { "$hostname:/opt/epoch/":
    user    => 'root',
    keyfile => '/root/.ssh/id_rsa',
    source  => '/opt/epoch/',
    #recurse => true,
  }
}
