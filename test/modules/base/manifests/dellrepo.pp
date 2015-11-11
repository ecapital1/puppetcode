class base::dellrepo {
  exec { "dell_repo":
      command => "/usr/bin/wget -q -O - http://linux.dell.com/repo/hardware/latest/bootstrap.cgi > bootstrap.cgi",
      command => "/bin/bash /root/bootstrap.cgi",
      creates => '/opt/dell/'
  }
}
