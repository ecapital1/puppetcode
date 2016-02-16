class base::python {
  class { '::python':
    version => 'system',
    pip     => 'present',
  }
}
