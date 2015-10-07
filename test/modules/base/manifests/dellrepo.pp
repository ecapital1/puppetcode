class base::dellrepo {
  exec { "dell_repo":
      command => "wget -q -O - http://linux.dell.com/repo/hardware/latest/bootstrap.cgi | bash",
      path    => "/usr/bin/",
  }
}
