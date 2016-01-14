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
  package { 'wireshark':
        ensure   => latest,
        provider => 'chocolatey',
  }
  package { 'ccleaner':
        ensure   => latest,
        provider => 'chocolatey',
  }
  package { 'atom':
        ensure   => latest,
        provider => 'chocolatey',
  }
  package { 'powershell':
        ensure   => latest,
        provider => 'chocolatey',
  }
  package { 'dotnet4.5':
        ensure   => latest,
        provider => 'chocolatey',
  }
  package { 'vcredist2013':
        ensure   => latest,
        provider => 'chocolatey',
  }
}
