class windows::choco {
  class {'::chocolatey':}
}
Package { provider => chocolatey, }
package { 'notepadplusplus':
  ensure   => latest,
  provider => 'chocolatey',
}
