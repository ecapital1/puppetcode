class windowsbase::choco {
  class {'::chocolatey':}
  package { 'git':
  	ensure   => latest,
  	provider => 'chocolatey',
  }
  package { '7zip':
        ensure   => latest,
        provider => 'chocolatey',
  }
  package { 'google-chrome-x64':
        ensure   => latest,
        provider => 'chocolatey',
  }
  package { 'putty':
        ensure   => latest,
        provider => 'chocolatey',
  }
  package { 'keepass':
        ensure   => latest,
        provider => 'chocolatey',
  }
  package { 'python2':
        ensure   => latest,
        provider => 'chocolatey',
  }

}
