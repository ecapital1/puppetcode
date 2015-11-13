class windows::choco {
  class {'::chocolatey':}
}
case $operatingsystem {
  'windows':
    Package { provider => chocolatey, }
}
package { 'notepadplusplus':
  ensure   => latest,
  provider => 'chocolatey',
}
