class base::dellrepo {
  exec { "dell_repo":
      command => "/usr/bin/wget -q -O - http://linux.dell.com/repo/hardware/latest/bootstrap.cgi > bootstrap.cgi",
      #path    => "/usr/bin/",
  }
  exec { "dell_repo_install":
      command => "/bin/bash /root/bootstrap.cgi",
      #path    => "/bin/"
    }
}
