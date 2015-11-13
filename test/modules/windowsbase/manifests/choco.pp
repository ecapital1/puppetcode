class windowsbase::choco {
  class {'::chocolatey':}
}
package { provider => chocolatey, }
package { 'notepadplusplus':
  ensure   => latest,
  provider => 'chocolatey',
}
