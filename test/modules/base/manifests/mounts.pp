class base::mounts {
  class { '::fstab': }
    fstab::mount { '/Data/rdb':
      ensure  => 'directory'
      ensure  => 'mounted',
      device  => 'epcau-srv-003:/Data/rdb/',
      options => 'auto',
      fstype  => 'nfs',
    }
}
