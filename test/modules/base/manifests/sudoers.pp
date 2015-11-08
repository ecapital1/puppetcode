class base::sudoers {
  class { '::sudo':
    config_file_replace => false,
  }
  sudo::conf { 'admins':
    priority => 10,
    content  => "%admins ALL=(ALL) NOPASSWD: ALL",
  }
}
